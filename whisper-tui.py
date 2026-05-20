#!/usr/bin/env python3
"""
daemon-whisper TUI Companion App
Optional companion for daemon-whisper - NOT required for core functionality
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Try to import rich/TUI libraries
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.layout import Layout
    from rich import box
except ImportError:
    print("Error: Required libraries not found.")
    print("Install with: pip install rich")
    sys.exit(1)

try:
    import psutil
except ImportError:
    print("Warning: psutil not found. CPU stats will be limited.")
    print("Install with: pip install psutil")
    psutil = None


class WhisperConfig:
    """Manages Whisper configuration and paths"""

    def __init__(self):
        self.home = Path.home()
        self.whisper_dir = self.home / "whisper.cpp"
        self.models_dir = self.whisper_dir / "models"
        self.script_path = self.home / ".local" / "bin" / "whisper-stt.sh"
        self.log_file = Path("/tmp/whisper_stt_log.json")

        # Model definitions (size, parameters, download name)
        self.models = {
            "tiny.en": {"params": "39 M", "size_mb": 78, "vram": "~1 GB", "speed": "~10x", "type": "en"},
            "tiny": {"params": "39 M", "size_mb": 78, "vram": "~1 GB", "speed": "~10x", "type": "multi"},
            "base.en": {"params": "74 M", "size_mb": 148, "vram": "~1 GB", "speed": "~7x", "type": "en"},
            "base": {"params": "74 M", "size_mb": 148, "vram": "~1 GB", "speed": "~7x", "type": "multi"},
            "small.en": {"params": "244 M", "size_mb": 466, "vram": "~2 GB", "speed": "~4x", "type": "en"},
            "small": {"params": "244 M", "size_mb": 466, "vram": "~2 GB", "speed": "~4x", "type": "multi"},
            "medium.en": {"params": "769 M", "size_mb": 1536, "vram": "~5 GB", "speed": "~2x", "type": "en"},
            "medium": {"params": "769 M", "size_mb": 1536, "vram": "~5 GB", "speed": "~2x", "type": "multi"},
            "large": {"params": "1550 M", "size_mb": 3072, "vram": "~10 GB", "speed": "1x", "type": "multi"},
            "turbo": {"params": "809 M", "size_mb": 1638, "vram": "~6 GB", "speed": "~8x", "type": "multi"},
        }


class WhisperTUI:
    """Main TUI application"""

    def __init__(self):
        self.console = Console()
        self.config = WhisperConfig()
        self.current_model = self._get_current_model()
        self.installed_models = self._get_installed_models()
        self.last_transcription = self._get_last_transcription()

    def _get_current_model(self) -> Optional[str]:
        """Extract current model from whisper-stt.sh"""
        try:
            if not self.config.script_path.exists():
                return None

            with open(self.config.script_path, 'r') as f:
                for line in f:
                    if line.strip().startswith('MODEL=') and not line.strip().startswith('#'):
                        # Extract model name from path
                        model_path = line.split('=')[1].strip().strip('"').strip("'")
                        model_name = Path(model_path).name.replace('ggml-', '').replace('.bin', '')
                        return model_name
        except Exception as e:
            pass
        return None

    def _get_installed_models(self) -> List[str]:
        """List installed models"""
        installed = []
        if self.config.models_dir.exists():
            for model_file in self.config.models_dir.glob("ggml-*.bin"):
                model_name = model_file.name.replace('ggml-', '').replace('.bin', '')
                installed.append(model_name)
        return sorted(installed)

    def _get_last_transcription(self) -> Optional[Dict]:
        """Read last transcription log"""
        try:
            if self.config.log_file.exists():
                with open(self.config.log_file, 'r') as f:
                    logs = json.load(f)
                    if logs:
                        return logs[-1]  # Return most recent
        except Exception:
            pass
        return None

    def show_header(self):
        """Display application header"""
        header = "[bold cyan]daemon-whisper TUI[/bold cyan]"
        subtitle = "[dim]Optional companion for daemon-whisper[/dim]"
        self.console.print(Panel(header + "\n" + subtitle, box.box.DOUBLE, style="cyan"))

    def show_current_status(self):
        """Display current status panel"""
        status_lines = []

        # Current model
        if self.current_model:
            model_info = self.config.models.get(self.current_model, {})
            status_lines.append(f"[bold green]Current Model:[/bold green] {self.current_model}")
            if model_info:
                status_lines.append(f"  Parameters: {model_info.get('params', 'N/A')}")
                status_lines.append(f"  Size: {model_info.get('size_mb', 'N/A')} MB")
                status_lines.append(f"  VRAM: {model_info.get('vram', 'N/A')}")
                status_lines.append(f"  Speed: {model_info.get('speed', 'N/A')}")
                status_lines.append(f"  Type: {'English-only' if model_info.get('type') == 'en' else 'Multilingual'}")
        else:
            status_lines.append("[bold red]No model configured![/bold red]")
            status_lines.append("  Script not found or MODEL not set")

        # Installation status
        status_lines.append(f"\n[bold]Installed Models:[/bold] {len(self.installed_models)}/{len(self.config.models)}")

        self.console.print(Panel("\n".join(status_lines), title="[bold]Status[/bold]", box.box.ROUNDED))

    def show_last_transcription(self):
        """Display last transcription info"""
        if self.last_transcription:
            log = self.last_transcription
            lines = [
                f"[bold]Time:[/bold] {log.get('timestamp', 'N/A')}",
                f"[bold]Model:[/bold] {log.get('model', 'N/A')}",
                f"[bold]Audio Duration:[/bold] {log.get('audio_duration', 'N/A')}s",
                f"[bold]Processing Time:[/bold] {log.get('processing_time', 'N/A')}s",
                f"[bold]CPU Usage:[/bold] {log.get('cpu_usage', 'N/A')}%",
                f"[bold]Text:[/bold] {log.get('text', 'N/A')[:60]}...",
            ]
            self.console.print(Panel("\n".join(lines), title="[bold]Last Transcription[/bold]", box.box.ROUNDED))
        else:
            self.console.print(Panel("[dim]No transcriptions logged yet[/dim]", title="[bold]Last Transcription[/bold]", box.box.ROUNDED))

    def show_model_list(self):
        """Display all available models"""
        table = Table(title="Available Models", box.box.ROUNDED)
        table.add_column("Model", style="cyan")
        table.add_column("Params", style="magenta")
        table.add_column("Size", style="green")
        table.add_column("VRAM", style="blue")
        table.add_column("Speed", style="yellow")
        table.add_column("Type", style="red")
        table.add_column("Status", style="bold")

        for name, info in self.config.models.items():
            installed = "[green]Installed[/green]" if name in self.installed_models else "[dim]Not installed[/dim]"
            is_current = " [cyan](current)[/cyan]" if name == self.current_model else ""
            type_str = "English" if info["type"] == "en" else "Multi"

            table.add_row(
                name + is_current,
                info["params"],
                f"{info['size_mb']} MB",
                info["vram"],
                info["speed"],
                type_str,
                installed
            )

        self.console.print(table)

    def show_system_info(self):
        """Display system information"""
        lines = []

        # CPU info
        if psutil:
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            cpu_count = psutil.cpu_count()

            lines.append(f"[bold]CPU Usage:[/bold] {cpu_percent}%")
            lines.append(f"[bold]CPU Frequency:[/bold] {cpu_freq.current:.0f} MHz" if cpu_freq else "[bold]CPU Frequency:[/bold] N/A")
            lines.append(f"[bold]CPU Cores:[/bold] {cpu_count}")

            # Memory info
            mem = psutil.virtual_memory()
            lines.append(f"[bold]Memory:[/bold] {mem.percent}% used ({mem.available // 1024 // 1024} MB free)")

        # Check for required tools
        lines.append("\n[bold]Required Tools:[/bold]")
        tools = [
            ("whisper-cli", self.config.whisper_dir / "build" / "bin" / "whisper-cli"),
            ("wtype", None),
            ("arecord", None),
            ("notify-send", None),
        ]

        for tool, path in tools:
            if path:
                exists = "[green]✓[/green]" if path.exists() else "[red]✗[/red]"
            else:
                # Check if tool is in PATH
                exists = "[green]✓[/green]" if subprocess.run(["which", tool], capture_output=True).returncode == 0 else "[red]✗[/red]"
            lines.append(f"  {exists} {tool}")

        self.console.print(Panel("\n".join(lines), title="[bold]System Information[/bold]", box.box.ROUNDED))

    def download_model(self, model_name: str):
        """Download a model using whisper.cpp's script"""
        if model_name not in self.config.models:
            self.console.print(f"[red]Error: Unknown model '{model_name}'[/red]")
            return False

        if model_name in self.installed_models:
            self.console.print(f"[yellow]Model {model_name} is already installed.[/yellow]")
            return Confirm.ask("Download anyway?", default=False)

        self.console.print(f"[cyan]Downloading {model_name}...[/cyan]")

        try:
            result = subprocess.run(
                [self.config.whisper_dir / "models" / "download-ggml-model.sh", model_name],
                cwd=self.config.whisper_dir,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                self.console.print(f"[green]✓ Model {model_name} downloaded successfully![/green]")
                self.installed_models = self._get_installed_models()
                return True
            else:
                self.console.print(f"[red]✗ Failed to download {model_name}[/red]")
                self.console.print(f"[dim]{result.stderr}[/dim]")
                return False
        except Exception as e:
            self.console.print(f"[red]✗ Error: {e}[/red]")
            return False

    def set_model(self, model_name: str):
        """Set the active model in whisper-stt.sh"""
        if model_name not in self.installed_models:
            self.console.print(f"[red]Error: Model {model_name} is not installed.[/red]")
            return False

        try:
            with open(self.config.script_path, 'r') as f:
                lines = f.readlines()

            # Update MODEL line
            for i, line in enumerate(lines):
                if line.strip().startswith('MODEL='):
                    # Comment out all MODEL lines
                    lines[i] = '#' + line if not line.strip().startswith('#') else line

            # Find first commented MODEL line or add new one
            for i, line in enumerate(lines):
                if line.strip().startswith('#MODEL='):
                    lines[i] = f'MODEL="$HOME/whisper.cpp/models/ggml-{model_name}.bin"\n'
                    break
            else:
                # Add after configuration section
                for i, line in enumerate(lines):
                    if '# Configuration' in line:
                        lines.insert(i + 1, f'MODEL="$HOME/whisper.cpp/models/ggml-{model_name}.bin"\n')
                        break

            with open(self.config.script_path, 'w') as f:
                f.writelines(lines)

            self.current_model = model_name
            self.console.print(f"[green]✓ Model set to {model_name}[/green]")
            self.console.print("[dim]You may need to reload any running instances.[/dim]")
            return True
        except Exception as e:
            self.console.print(f"[red]✗ Error: {e}[/red]")
            return False

    def run_menu(self):
        """Main menu loop"""
        while True:
            self.console.clear()
            self.show_header()
            self.show_current_status()
            self.show_last_transcription()

            choices = [
                "View all models",
                "Download a model",
                "Switch model",
                "View system info",
                "Refresh status",
                "Exit"
            ]

            self.console.print("\n")
            for i, choice in enumerate(choices, 1):
                self.console.print(f"[cyan]{i}.[/cyan] {choice}")

            choice = Prompt.ask("\nSelect option", choices=[str(i) for i in range(1, len(choices) + 1)])

            if choice == "1":
                self.console.clear()
                self.show_header()
                self.show_model_list()
                Prompt.ask("\nPress Enter to continue")

            elif choice == "2":
                self.console.clear()
                self.show_header()
                self.show_model_list()

                model_name = Prompt.ask("\nEnter model name to download", choices=list(self.config.models.keys()))
                self.download_model(model_name)
                Prompt.ask("\nPress Enter to continue")

            elif choice == "3":
                if not self.installed_models:
                    self.console.print("[yellow]No models installed. Download a model first.[/yellow]")
                    Prompt.ask("\nPress Enter to continue")
                    continue

                self.console.clear()
                self.show_header()
                self.console.print("\n[bold]Installed Models:[/bold]")
                for model in self.installed_models:
                    marker = " [cyan](current)[/cyan]" if model == self.current_model else ""
                    self.console.print(f"  • {model}{marker}")

                model_name = Prompt.ask("\nSelect model", choices=self.installed_models)
                self.set_model(model_name)
                Prompt.ask("\nPress Enter to continue")

            elif choice == "4":
                self.console.clear()
                self.show_header()
                self.show_system_info()
                Prompt.ask("\nPress Enter to continue")

            elif choice == "5":
                self.current_model = self._get_current_model()
                self.installed_models = self._get_installed_models()
                self.last_transcription = self._get_last_transcription()
                self.console.print("[green]✓ Status refreshed[/green]")
                Prompt.ask("\nPress Enter to continue")

            elif choice == "6":
                self.console.print("[cyan]Goodbye![/cyan]")
                break


def main():
    """Main entry point"""
    tui = WhisperTUI()
    tui.run_menu()


if __name__ == "__main__":
    main()
