"""Example plugin demonstrating the VoltMind plugin system."""

from typing import Dict, Any, Optional
from rich.console import Console

# These imports would normally be available when the plugin is loaded by VoltMind CLI
# For development purposes, we'll create minimal interfaces here
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from dataclasses import dataclass
from rich.console import Console


@dataclass
class PluginInfo:
    """Plugin metadata."""
    name: str
    version: str
    description: str
    author: str
    commands: List[str]
    entry_point: str


class ICommand(ABC):
    """Interface for all CLI commands."""
    
    @abstractmethod
    def execute(self, **kwargs: Any) -> Optional[Any]:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_help(self) -> str:
        pass


class BaseCommand(ICommand):
    """Base implementation of ICommand interface."""

    def __init__(self, name: str, help_text: str):
        self._name = name
        self._help = help_text

    def get_name(self) -> str:
        return self._name

    def get_help(self) -> str:
        return self._help

    def execute(self, **kwargs: Any) -> Optional[Any]:
        raise NotImplementedError("Subclasses must implement execute method")


class IPlugin(ABC):
    """Interface for all plugins."""

    @abstractmethod
    def get_info(self) -> PluginInfo:
        pass

    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def get_commands(self) -> Dict[str, ICommand]:
        pass


class GreetCommand(BaseCommand):
    """Example plugin command that greets with a custom message."""

    def __init__(self):
        super().__init__(
            name="greet",
            help_text="Greet with a custom message from the example plugin"
        )
        self.console = Console()

    def execute(self, **kwargs: Any) -> Optional[Any]:
        """Execute the greet command."""
        name = kwargs.get('name', 'Friend')
        style = kwargs.get('style', 'friendly')
        
        if style == 'formal':
            message = f"Good day, {name}. I hope you are well."
        elif style == 'casual':
            message = f"Hey {name}! What's up?"
        else:  # friendly
            message = f"Hello there, {name}! Nice to see you!"
        
        self.console.print(f"🤖 [bold blue]{message}[/bold blue]")
        self.console.print("[dim]This message is brought to you by the Example Plugin![/dim]")
        
        return message


class CountCommand(BaseCommand):
    """Example command that counts to a specified number."""

    def __init__(self):
        super().__init__(
            name="count",
            help_text="Count from 1 to a specified number"
        )
        self.console = Console()

    def execute(self, **kwargs: Any) -> Optional[Any]:
        """Execute the count command."""
        max_num = kwargs.get('max', 5)
        
        try:
            max_num = int(max_num)
            if max_num < 1:
                self.console.print("[red]Please provide a positive number[/red]")
                return None
                
            if max_num > 100:
                self.console.print("[yellow]That's a big number! Limiting to 100[/yellow]")
                max_num = 100
                
            self.console.print(f"🔢 Counting to {max_num}:")
            for i in range(1, max_num + 1):
                self.console.print(f"  {i}")
                
            self.console.print(f"✅ Finished counting to {max_num}!")
            return max_num
            
        except ValueError:
            self.console.print("[red]Please provide a valid number[/red]")
            return None


class Plugin(IPlugin):
    """Example plugin implementation."""

    def __init__(self):
        self._commands: Dict[str, ICommand] = {}

    def get_info(self) -> PluginInfo:
        """Get plugin information."""
        return PluginInfo(
            name="example-plugin",
            version="1.0.0",
            description="An example plugin demonstrating VoltMind's plugin system",
            author="VoltMind Team",
            commands=["greet", "count"],
            entry_point="plugin.Plugin"
        )

    def initialize(self) -> None:
        """Initialize the plugin."""
        self._commands = {
            "greet": GreetCommand(),
            "count": CountCommand()
        }

    def get_commands(self) -> Dict[str, ICommand]:
        """Get available commands from this plugin."""
        return self._commands.copy()
