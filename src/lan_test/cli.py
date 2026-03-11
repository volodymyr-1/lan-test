"""cli.py - Typer CLI interface."""
import asyncio
import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint

app     = typer.Typer(help="lan-test CLI — monitoring for langgraph-lab pipeline")
console = Console()


@app.command()
def status():
    """Check health of all local AI services."""
    from lan_test.monitor import check_all
    from lan_test.models import ServiceStatus

    result = asyncio.run(check_all())

    table = Table(title="Service Health", show_header=True)
    table.add_column("Service",    style="bold")
    table.add_column("Status")
    table.add_column("Latency")
    table.add_column("URL",        style="dim")

    icons = {ServiceStatus.OK: "✅", ServiceStatus.DEGRADED: "⚠️", ServiceStatus.DOWN: "❌"}
    for svc in result.services:
        latency = f"{svc.latency_ms:.0f}ms" if svc.latency_ms else "—"
        table.add_row(svc.name, f"{icons[svc.status]} {svc.status}", latency, svc.url)

    console.print(table)
    rprint(f"\n[bold]Overall:[/bold] {icons[result.status]} {result.status}")


@app.command()
def history(limit: int = typer.Option(20, help="Number of records")):
    """Show request history from SQLite."""
    from lan_test.db import get_history

    records = asyncio.run(get_history(limit))
    if not records:
        rprint("[yellow]No history yet.[/yellow]")
        return

    table = Table(title=f"Last {limit} requests", show_header=True)
    table.add_column("ID",       style="dim")
    table.add_column("Question", max_width=50)
    table.add_column("Provider")
    table.add_column("Quality")
    table.add_column("Saved")
    table.add_column("Latency")

    for r in records:
        saved = "✅" if r.saved else "—"
        q_color = "green" if r.quality >= 0.7 else "yellow" if r.quality >= 0.4 else "red"
        table.add_row(
            str(r.id), r.question[:50],
            r.provider, f"[{q_color}]{r.quality:.1f}[/{q_color}]",
            saved, f"{r.latency_ms:.0f}ms",
        )
    console.print(table)


@app.command()
def stats():
    """Show aggregate statistics."""
    from lan_test.db import get_stats

    data = asyncio.run(get_stats())
    rprint(f"\n[bold]Total requests:[/bold] {data['total']}")
    rprint(f"[bold]Saved patterns:[/bold] {data['saved']}")
    rprint(f"[bold]Avg quality:   [/bold] {data['avg_quality']}")
    rprint("\n[bold]By provider:[/bold]")
    for provider, count in data["by_provider"].items():
        rprint(f"  {provider}: {count}")


if __name__ == "__main__":
    app()
