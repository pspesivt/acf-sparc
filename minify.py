#!/usr/bin/env python
"""
Context Window Optimization Script

This script synchronizes files from src/.roo to templates/base/.roo, compressing
the content using external LLM compression techniques.

It can process entire directories or individual files as needed.
"""

import os
import sys
import re
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Union

import typer
import tiktoken
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich import box

# Initialize Rich console
console = Console()

def compress_with_llm(content: str, endpoint: str, api_key: str, model: str, progress=None, task_id=None) -> Tuple[str, Dict[str, Any]]:
    """
    Compress content using an external LLM via OpenAI-compatible API.
    
    This function calls an external LLM to optimize the prompt while preserving
    all factual information and instructions.
    """
    try:
        # Count tokens before compression
        enc = tiktoken.get_encoding("o200k_base")
        tokens_before = len(enc.encode(content))
        
        # Initialize OpenAI client with custom endpoint
        import openai
        client = openai.OpenAI(
            base_url=endpoint,
            api_key=api_key
        )
        
        # System prompt for compression
        system_prompt = """Your goal is to optimize the number of tokens consumed by the text provided by user minimizing loss of precision and technical details when the output text will be interpreted by LLM instead of human. Analyze the complete text and stick to the pseudo-alogithm below and return ONLY output and nothing else. The output text does not have to be readable by humans, and use every opportunity to reduce the number of tokens used in the output while keeping it understandable by machine, while sticking to the algorithm below.
compress(input)->output:
  preserve_exact={headers,titles,paths,protocols,names,identifiers,values,code,xml_tools(<*>),xml_contracts}
  preserve_semantic={structure,hierarchy,logic,relationships,content}
  remove={formatting(**,__,###),redundancy,filler,fluff,verbosity,human_markup,meta_commentary}
  apply={merge_similar,compact_syntax,implicit_structure}
  protected_patterns={headers,titles,xml_tools(<*>),</*>,xml_contracts,tool_invocations}
  effort=ultrathink
  constraint=lossless_technical,lossless_xml_contracts
  output_format=direct_start_no_preamble
  forbidden={introduction,commentary,evaluation,transition_text,acknowledgment}
  special_rule=NEVER_modify_xml_tool_syntax
  return=compressed_content_only_no_surrounding_text
        """
        
        if progress and task_id:
            progress.update(task_id, description=f"[cyan]Calling LLM API ({model})[/]")
        else:
            console.print(f"[cyan]Calling external LLM API ({model}) for compression...[/]")
            
        # Determine appropriate temperature based on model name
        # Check for any variation of o3/o4 models (o4-mini, o3:flex, etc.)
        is_o_model = re.search(r'o[34][\s\-:_]?', model.lower()) is not None
        temperature = 1.0 if is_o_model else 0.2

        # Call the LLM API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content}
            ],
            temperature=temperature,  # Adjusted based on model type
        )
        
        # Log the temperature used
        if progress and task_id:
            progress.update(task_id, description=f"[cyan]Using temperature: {temperature} for model: {model}[/]")
        else:
            console.print(f"[cyan]Using temperature: {temperature} for model: {model}[/]")
        
        # Extract compressed content from response
        compressed_content = response.choices[0].message.content
        
        # Count tokens after compression
        tokens_after = len(enc.encode(compressed_content))
        
        stats = {
            'tokens_before': tokens_before,
            'tokens_after': tokens_after,
            'token_reduction': tokens_before - tokens_after,
            'token_ratio': tokens_before / max(tokens_after, 1)
        }
        
        if progress and task_id:
            progress.update(task_id, description=f"[green]LLM compression complete[/]")
        else:
            console.print(f"[green]LLM compression:[/] {tokens_before} → {tokens_after} tokens ([bold cyan]{stats['token_ratio']:.2f}x[/])")
        
        return compressed_content, stats
        
    except Exception as e:
        if progress and task_id:
            progress.update(task_id, description=f"[red]LLM compression error: {e}[/]")
        else:
            console.print(f"[red]Error in LLM compression: {e}[/]")
        # Count tokens in original content for consistent stats
        enc = tiktoken.get_encoding("cl100k_base")
        tokens = len(enc.encode(content))
        stats = {
            'tokens_before': tokens,
            'tokens_after': tokens,
            'token_reduction': 0,
            'token_ratio': 1.0
        }
        return content, stats


def compress_content(content: str, 
                    use_llm: bool = False,
                    llm_endpoint: str = "",
                    llm_api_key: str = "",
                    llm_model: str = "",
                    progress=None,
                    task_id=None) -> Tuple[str, Dict[str, Any]]:
    """
    Apply compression to content using external LLM compression (if enabled).
    
    Returns compressed content and statistics.
    """
    original_size = len(content)
    current_content = content
    stats = {}
    
    # External LLM compression (if enabled)
    if use_llm:
        try:
            if progress and task_id:
                progress.update(task_id, description="[cyan]Applying external LLM compression...[/]")
            else:
                console.print("[cyan]Applying external LLM compression...[/]")
            
            current_content, llm_stats = compress_with_llm(
                current_content, llm_endpoint, llm_api_key, llm_model, progress, task_id
            )
            stats.update(llm_stats)
        except Exception as e:
            if progress and task_id:
                progress.update(task_id, description=f"[red]Error in external LLM compression: {e}[/]")
            else:
                console.print(f"[red]Error in external LLM compression: {e}[/]")
                console.print("[yellow]Falling back to original content[/]")
    
    final_compressed = current_content
    final_size = len(final_compressed)
    
    # Calculate compression statistics
    final_stats = {
        'original_size': original_size,
        'final_size': final_size,
        'total_ratio': original_size / max(final_size, 1)
    }
    
    if use_llm:
        final_stats['llm_size'] = len(current_content)
        final_stats['llm_ratio'] = original_size / max(final_stats['llm_size'], 1)
        
        # Preserve token statistics from LLM compression
        if 'tokens_before' in stats:
            final_stats['tokens_before'] = stats['tokens_before']
        if 'tokens_after' in stats:
            final_stats['tokens_after'] = stats['tokens_after']
        if 'token_ratio' in stats:
            final_stats['token_ratio'] = stats['token_ratio']
    
    if progress and task_id:
        progress.update(task_id, description="[green]Compression complete[/]")
    
    return final_compressed, final_stats

def process_file(source_path: Path, target_path: Path, 
                use_llm: bool = False,
                llm_endpoint: str = "",
                llm_api_key: str = "",
                llm_model: str = "",
                progress=None,
                task_id=None,
                source_dir_path: Path = None) -> Dict[str, Any]:
    """Process a single file, compressing it and saving to target path."""
    start_time = time.time()
    
    try:
        # Calculate relative path for display
        rel_path = source_path.relative_to(source_dir_path) if source_dir_path else source_path
        
        # Read source content
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if progress and task_id:
            progress.update(task_id, description=f"[cyan]Compressing file[/] [blue]{rel_path}[/]")
        
        # Track time for compression
        method_times = {
            'llm': 0.0
        }
        
        # Compress content
        if use_llm:
            llm_start = time.time()
        
        compressed_content, stats = compress_content(
            content,
            use_llm,
            llm_endpoint,
            llm_api_key,
            llm_model,
            progress,
            task_id
        )
        
        # Create target directory if it doesn't exist
        os.makedirs(target_path.parent, exist_ok=True)
        
        # Write compressed content to target file
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(compressed_content)
        
        # Calculate total processing time
        processing_time = time.time() - start_time
        
        if progress and task_id:
            ratio = stats['total_ratio']
            ratio_color = "green" if ratio > 1.5 else "yellow" if ratio > 1.0 else "red"
            time_str = format_time(processing_time)
            rel_path = source_path.relative_to(source_dir_path) if source_dir_path else source_path
            progress.update(task_id, description=f"[green]✓[/] [blue]{rel_path}[/] Saved ([{ratio_color}]{ratio:.2f}x[/]) in {time_str}")
        
        return {
            'file': str(source_path),
            'status': 'success',
            'processing_time': processing_time,
            **stats
        }
    except Exception as e:
        if progress and task_id:
            rel_path = source_path.relative_to(source_dir_path) if source_dir_path else source_path
            progress.update(task_id, description=f"[red]✗ [blue]{rel_path}[/] Error: {e}[/]")
        
        return {
            'file': str(source_path),
            'status': 'error',
            'error': str(e)
        }

def format_time(seconds: float) -> str:
    """Format time in seconds to a human-readable string"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"

def get_time_color(seconds: float) -> str:
    """Get color based on processing time"""
    if seconds < 1:
        return "bright_green"
    elif seconds < 5:
        return "green"
    elif seconds < 15:
        return "green3"
    elif seconds < 30:
        return "yellow"
    else:
        return "red"

def get_ratio_color(ratio: float) -> str:
    """Get color based on compression ratio"""
    if ratio >= 2.0:
        return "bright_green"
    elif ratio >= 1.5:
        return "green"
    elif ratio >= 1.2:
        return "green3"
    elif ratio > 1.0:
        return "yellow"
    else:
        return "red"

def print_fancy_header():
    """Print a fancy header for the script"""
    title = "Context Window Optimizer"
    
    console.print()
    console.print(Panel.fit(
        Text(title, style="bold white on blue", justify="center"), 
        border_style="blue",
        padding=(1, 10),
        title="[bold yellow]ACF-SPARC Framework[/]",
        subtitle="[bold cyan]v1.0[/]"
    ))
    console.print()

def main(
    source_dir: str = typer.Option("src", help="Source directory containing instruction files"),
    target_dir: str = typer.Option("templates/base/.roo", help="Target directory for compressed files"),
    file_path: Optional[str] = typer.Option(None, "--file", "-f", help="Process a single file instead of a directory"),
    file_pattern: str = typer.Option("**/*.md", help="File pattern to include when processing directory (e.g., '**/*.md' for markdown files)"),
    exclude_patterns: List[str] = typer.Option(["rules-docs/examples/"], help="Patterns to exclude from processing"),
    use_llm: bool = typer.Option(False, help="Enable external LLM compression (disabled by default)"),
    llm_endpoint: str = typer.Option(None, help="OpenAI-compatible API endpoint"),
    llm_model: str = typer.Option(None, help="Model to use for LLM compression")
):
    """
    Synchronize files from source directory to target directory,
    compressing the content using external LLM compression methods if enabled.
    By default, it just copies files without compression.
    
    Can process an entire directory or a single file:
    - For directories: All matching files will be processed according to file_pattern
    - For single files: Use --file/-f option to specify a single file to process
    """
    print_fancy_header()
    
    # Load environment variables
    load_dotenv()
    
    # Handle API endpoint, model, and key with proper precedence
    # Precedence: CLI parameters > Environment variables > Default values
    if llm_endpoint is None:
        llm_endpoint = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        
    if llm_model is None:
        llm_model = os.environ.get("LLM_MODEL", "gpt-4o")
    
    # Handle API key from environment
    llm_api_key = ""
    if use_llm:
        llm_api_key = os.environ.get("OPENAI_API_KEY", "")
        if not llm_api_key:
            console.print("[bold red]Error:[/] OPENAI_API_KEY environment variable is required for LLM compression")
            raise typer.Exit(code=1)
        
        # Log the LLM configuration
        console.print(f"Using LLM endpoint: [cyan]{llm_endpoint}[/]")
        console.print(f"Using LLM model: [cyan]{llm_model}[/]")
    
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    # Create target directory if it doesn't exist
    if not target_path.exists():
        console.print(f"Creating target directory [cyan]{target_dir}[/]")
        os.makedirs(target_path, exist_ok=True)
    
    # Determine if we're processing a single file or a directory
    if file_path:
        # Process single file mode
        source_file = Path(file_path)
        if not source_file.exists() or not source_file.is_file():
            console.print(f"[bold red]Error:[/] File [cyan]{file_path}[/] does not exist or is not a file")
            raise typer.Exit(code=1)
        
        # Calculate target path based on source directory structure
        if source_file.is_relative_to(source_path):
            # File is within source directory, maintain directory structure
            rel_path = source_file.relative_to(source_path)
            target_file = target_path / rel_path
        else:
            # File is outside source directory, just use the filename
            target_file = target_path / source_file.name
        
        source_files = [source_file]
        console.print(f"Processing single file: [blue]{source_file}[/] → [green]{target_file}[/]")
    else:
        # Directory processing mode
        if not source_path.exists():
            console.print(f"[bold red]Error:[/] Source directory [cyan]{source_dir}[/] does not exist")
            raise typer.Exit(code=1)
        
        # Find all files matching the pattern in source directory
        if file_pattern == "**/*.md":
            # Optimization for all markdown files
            source_files = list(source_path.rglob("*.md"))
        else:
            # For other patterns, including specific markdown files like "**/rules.md"
            source_files = list(source_path.glob(file_pattern))
    
        # Filter out excluded patterns
        source_files = [
            f for f in source_files 
            if f.is_file() and not any(exclude in str(f) for exclude in exclude_patterns)
        ]
    
    if not source_files:
        console.print(f"[yellow]No files found in {source_dir}[/]")
        return
    
    console.print(f"Found [bold cyan]{len(source_files)}[/] files in [blue]{source_dir}[/]")
    console.print()
    
    # Create configuration panel
    config_table = Table(show_header=False, box=box.ROUNDED)
    config_table.add_column("Setting", style="bold cyan")
    config_table.add_column("Value", style="yellow")
    
    config_table.add_row("Source Directory", source_dir)
    config_table.add_row("Target Directory", target_dir)
    config_table.add_row("File Pattern", file_pattern)
    config_table.add_row("Excluded Patterns", ", ".join(exclude_patterns))
    config_table.add_row("External LLM", "✅ Enabled" if use_llm else "❌ Disabled")
    if use_llm:
        config_table.add_row("LLM Model", llm_model)
    
    console.print(Panel(config_table, title="[bold]Configuration[/]", border_style="blue"))
    console.print()
    
    # Start timing the overall process
    overall_start_time = time.time()
    
    # Process each file with fancy progress bar
    results = []
    
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        overall_task = progress.add_task("[bold cyan]Processing files...", total=len(source_files))
        
        for source_file in source_files:
            if file_path:
                # We're in single file mode, target_file is already set
                if source_file.is_relative_to(source_path):
                    # File is within source directory, maintain directory structure
                    rel_path = source_file.relative_to(source_path)
                    target_file = target_path / rel_path
                else:
                    # File is outside source directory, just use the filename
                    target_file = target_path / source_file.name
                    rel_path = Path(source_file.name)  # For display purposes
            else:
                # Calculate the relative path (directory mode)
                rel_path = source_file.relative_to(source_path)
                target_file = target_path / rel_path
            
            # Display the relative path before starting compression
            file_task = progress.add_task(f"[blue]{rel_path}[/]", total=1.0)
            
            # Process the file
            result = process_file(
                source_file, 
                target_file,
                use_llm,
                llm_endpoint,
                llm_api_key,
                llm_model,
                progress,
                file_task,
                source_path
            )
            results.append(result)
            progress.update(file_task, completed=1.0)
            progress.update(overall_task, advance=1)
    
    # Print summary
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'error']
    
    console.print()
    summary_title = Text("Compression Summary", style="bold white on blue")
    console.print(Panel(summary_title, border_style="blue"))
    console.print()
    
    # Show active compression methods
    methods_table = Table(show_header=False, box=box.SIMPLE)
    methods_table.add_column("Method", style="bold cyan")
    methods_table.add_column("Status", style="yellow")
    
    methods_table.add_row("External LLM compression", "✅ Applied" if use_llm else "❌ Not used")
    
    console.print(methods_table)
    console.print()
    
    # Create a fancy table for the results
    table = Table(
        show_header=True,
        header_style="bold white on blue",
        box=box.ROUNDED,
        border_style="blue",
        title="Compression Results"
    )
    
    # Define table columns based on compression methods used
    table.add_column("File", style="blue")
    table.add_column("Original", justify="right", style="yellow")
    table.add_column("Final", justify="right", style="green")
    table.add_column("Ratio", justify="right")
    table.add_column("Time", justify="right", style="magenta")
    
    if use_llm:
        table.add_column("Tokens Before", justify="right", style="yellow")
        table.add_column("Tokens After", justify="right", style="green")
        table.add_column("Token Ratio", justify="right")
    
    total_original = 0
    total_final = 0
    
    for result in successful:
        # Get relative path from source_dir
        file_path = Path(result['file'])
        rel_path = file_path.relative_to(source_path)
        
        original = result['original_size']
        llm = result['llm_size']
        final = result['final_size']
        ratio = result['total_ratio']
        
        total_original += original
        total_final += final
        
        # Get color based on compression ratio
        ratio_style = get_ratio_color(ratio)
        
        # Get timing information
        processing_time = result.get('processing_time', 0)
        time_str = format_time(processing_time)
        time_style = get_time_color(processing_time)
        
        # Build table row
        row = [
            str(rel_path),
            f"{original:,}",
            f"{final:,}",
            Text(f"{ratio:.2f}x", style=ratio_style),
            Text(time_str, style=time_style)
        ]
        
        # Add token info if available from LLM compression
        if use_llm and 'tokens_before' in result and 'tokens_after' in result:
            tokens_before = result.get('tokens_before', 0)
            tokens_after = result.get('tokens_after', 0)
            token_ratio = tokens_before / max(tokens_after, 1)
            token_ratio_style = get_ratio_color(token_ratio)
            
            row.extend([
                f"{tokens_before:,}",
                f"{tokens_after:,}",
                Text(f"{token_ratio:.2f}x", style=token_ratio_style)
            ])
            
        table.add_row(*row)
    
    if successful:
        overall_ratio = total_original / max(total_final, 1)
        ratio_style = get_ratio_color(overall_ratio)
        
        # Calculate total processing time
        total_processing_time = sum([r.get('processing_time', 0) for r in successful])
        avg_processing_time = total_processing_time / max(len(successful), 1)
        
        # Format timing information
        total_time_str = format_time(total_processing_time)
        avg_time_str = format_time(avg_processing_time)
        
        # Create totals row
        total_row = [
            Text("TOTAL", style="bold white"),
            Text(f"{total_original:,}", style="bold yellow"),
            Text(f"{total_final:,}", style="bold green"),
            Text(f"{overall_ratio:.2f}x", style=f"bold {ratio_style}"),
            Text(total_time_str, style="bold magenta")
        ]
        
        # Add token info totals if LLM compression was used
        if use_llm:
            total_tokens_before = sum([r.get('tokens_before', 0) for r in successful if 'tokens_before' in r])
            total_tokens_after = sum([r.get('tokens_after', 0) for r in successful if 'tokens_after' in r])
            token_ratio = total_tokens_before / max(total_tokens_after, 1)
            token_ratio_style = get_ratio_color(token_ratio)
            
            total_row.extend([
                Text(f"{total_tokens_before:,}", style="bold yellow"),
                Text(f"{total_tokens_after:,}", style="bold green"),
                Text(f"{token_ratio:.2f}x", style=f"bold {token_ratio_style}")
            ])
        
        # Add the totals row with a special style
        table.add_row(*total_row, style="on blue")
    
    # Print the table
    console.print(table)
    
    # Print any failed files in a separate error panel if there were any
    if failed:
        console.print()
        error_table = Table(show_header=True, header_style="bold white on red", box=box.ROUNDED, border_style="red")
        error_table.add_column("File", style="yellow")
        error_table.add_column("Error", style="red")
        
        for result in failed:
            file_path = Path(result['file'])
            rel_path = file_path.relative_to(source_path)
            error_table.add_row(str(rel_path), result['error'])
        
        console.print(Panel(error_table, title="[bold]Failed Files[/]", border_style="red"))
    
    # Calculate overall execution time
    overall_execution_time = time.time() - overall_start_time
    execution_time_str = format_time(overall_execution_time)
    
    # Print timing summary
    console.print()
    time_table = Table(show_header=False, box=box.SIMPLE)
    time_table.add_column("Metric", style="bold cyan")
    time_table.add_column("Value", style="bold yellow")
    
    time_table.add_row("Total execution time", execution_time_str)
    
    if successful:
        files_per_second = len(successful) / overall_execution_time if overall_execution_time > 0 else 0
        time_table.add_row("Files per second", f"{files_per_second:.2f}")
        time_table.add_row("Average time per file", avg_time_str)
    
    console.print(Panel(time_table, title="[bold]Timing Information[/]", border_style="magenta"))
    
    # Print completion message
    console.print()
    if successful and not failed:
        console.print(Panel(
            f"[bold green]All {len(successful)} files processed successfully![/]\n"
            f"Overall compression ratio: [bold cyan]{overall_ratio:.2f}x[/]\n"
            f"Total processing time: [bold magenta]{execution_time_str}[/]",
            title="[bold]Compression Complete[/]",
            border_style="green"
        ))
    elif successful and failed:
        console.print(Panel(
            f"[bold yellow]Completed with some errors[/]\n"
            f"[green]{len(successful)}[/] files processed successfully\n"
            f"[red]{len(failed)}[/] files failed\n"
            f"Total processing time: [bold magenta]{execution_time_str}[/]",
            title="[bold]Compression Complete[/]",
            border_style="yellow"
        ))
    else:
        console.print(Panel(
            f"[bold red]All {len(failed)} files failed to process![/]\n"
            f"Total processing time: [bold magenta]{execution_time_str}[/]",
            title="[bold]Compression Failed[/]",
            border_style="red"
        ))

if __name__ == "__main__":
    typer.run(main)
