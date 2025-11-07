#!/usr/bin/env python3
"""
analyze.py - Deep codebase analysis for axiart
Extracts: complexity, coupling, structure
"""

import ast
import os
import json
from pathlib import Path
from collections import defaultdict

def calculate_cyclomatic_complexity(node):
    """Calculate cyclomatic complexity for a function."""
    complexity = 1
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            complexity += len(child.values) - 1
    return complexity

def analyze_file(filepath):
    """Deep analysis of a single Python file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            tree = ast.parse(content)
    except Exception as e:
        return None

    analysis = {
        'path': str(filepath),
        'name': os.path.basename(filepath),
        'loc': len([l for l in lines if l.strip() and not l.strip().startswith('#')]),
        'functions': [],
        'classes': [],
        'imports': [],
        'exports': [],
        'max_complexity': 0,
        'avg_complexity': 0,
    }

    # Extract functions and complexity
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            complexity = calculate_cyclomatic_complexity(node)
            analysis['functions'].append({
                'name': node.name,
                'complexity': complexity,
                'lineno': node.lineno,
            })
            analysis['max_complexity'] = max(analysis['max_complexity'], complexity)

            # Count public functions (exports)
            if not node.name.startswith('_'):
                analysis['exports'].append(node.name)

        elif isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            analysis['classes'].append({
                'name': node.name,
                'methods': methods,
                'method_count': len(methods),
            })
            # Classes are exports
            if not node.name.startswith('_'):
                analysis['exports'].append(node.name)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                # Track relative imports within codebase
                if node.module.startswith('.'):
                    analysis['imports'].append(node.module)
                elif node.module.startswith('axiart'):
                    analysis['imports'].append(node.module)

    if analysis['functions']:
        analysis['avg_complexity'] = sum(f['complexity'] for f in analysis['functions']) / len(analysis['functions'])

    return analysis

def resolve_import_to_file(imp, base_dir):
    """Resolve a module import to actual file path."""
    # Handle relative imports like '.svg_exporter' or '..svg_exporter'
    parts = imp.split('.')

    # Remove empty parts from leading dots
    module_parts = [p for p in parts if p]

    if not module_parts:
        return None

    # Try to find the file
    possible_paths = [
        Path(base_dir) / f"{module_parts[-1]}.py",
        Path(base_dir) / module_parts[-1] / "__init__.py",
    ]

    for path in possible_paths:
        if path.exists():
            return str(path)

    return None

def analyze_codebase(root_dir):
    """Analyze entire codebase."""
    files = []
    file_by_path = {}

    # Find all Python files
    for py_file in Path(root_dir).rglob('*.py'):
        if '__pycache__' in str(py_file) or '.venv' in str(py_file):
            continue

        analysis = analyze_file(py_file)
        if analysis:
            files.append(analysis)
            file_by_path[str(py_file)] = analysis

    # Build dependency graph (file -> file dependencies)
    dependencies = defaultdict(set)

    for file_data in files:
        file_path = file_data['path']
        file_dir = os.path.dirname(file_path)

        for imp in file_data['imports']:
            # Resolve import to actual file
            resolved = resolve_import_to_file(imp, file_dir)
            if resolved and resolved in file_by_path and resolved != file_path:
                dependencies[file_path].add(resolved)

    # Calculate coupling metrics
    afferent = defaultdict(int)  # How many depend on me
    efferent = defaultdict(int)  # How many I depend on

    for file_path, deps in dependencies.items():
        efferent[file_path] = len(deps)
        for dep in deps:
            afferent[dep] += 1

    # Add coupling and instability to file data
    for file_data in files:
        path = file_data['path']
        ca = afferent.get(path, 0)
        ce = efferent.get(path, 0)

        file_data['afferent_coupling'] = ca
        file_data['efferent_coupling'] = ce
        file_data['instability'] = ce / (ca + ce) if (ca + ce) > 0 else 0
        file_data['api_surface'] = len(file_data['exports'])

    # Convert dependencies to serializable format
    deps_serializable = {k: list(v) for k, v in dependencies.items()}

    return {
        'files': files,
        'dependencies': deps_serializable,
        'total_loc': sum(f['loc'] for f in files),
        'total_files': len(files),
        'avg_complexity': sum(f['avg_complexity'] for f in files) / len(files) if files else 0,
        'max_complexity': max((f['max_complexity'] for f in files), default=0),
    }

if __name__ == '__main__':
    result = analyze_codebase('./axiart')

    with open('analysis.json', 'w') as f:
        json.dump(result, f, indent=2)

    print(f"✓ Deep analysis complete")
    print(f"  Files analyzed: {result['total_files']}")
    print(f"  Total LOC: {result['total_loc']:,}")
    print(f"  Avg complexity: {result['avg_complexity']:.2f}")
    print(f"  Max complexity: {result['max_complexity']}")

    # Find hotspots
    complex_files = [f for f in result['files'] if f['max_complexity'] > 10]
    if complex_files:
        print(f"\n🔥 Complexity hotspots ({len(complex_files)} files):")
        for f in sorted(complex_files, key=lambda x: x['max_complexity'], reverse=True)[:5]:
            print(f"  {f['name']}: max={f['max_complexity']}, avg={f['avg_complexity']:.1f}")

    # Find god objects (high afferent coupling)
    god_objects = [f for f in result['files'] if f['afferent_coupling'] > 5]
    if god_objects:
        print(f"\n🎯 God objects ({len(god_objects)} files):")
        for f in sorted(god_objects, key=lambda x: x['afferent_coupling'], reverse=True):
            print(f"  {f['name']}: {f['afferent_coupling']} modules depend on it")

    # Summary stats
    total_deps = sum(len(deps) for deps in result['dependencies'].values())
    print(f"\n📊 Architecture:")
    print(f"  Total dependencies: {total_deps}")
    print(f"  Avg dependencies per file: {total_deps / result['total_files']:.1f}")
