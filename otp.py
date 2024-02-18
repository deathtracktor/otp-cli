"""
    CLI replacement for the passed away Authy Desktop app.
"""
import pathlib
import stat

import click
import pyotp
import pyperclip
from sqlitedict import SqliteDict
from tabulate import tabulate


@click.group()
@click.pass_context
def cli(ctx):
    """
    CLI for generating time-based OTP tokens.
    """
    secure_path = pathlib.Path.home() / 'totp.sqlite'
    ctx.obj = SqliteDict(secure_path)

@cli.command()
@click.argument('name')
@click.argument('key')
@click.option('--comment', default=None, help='Account comment/description.')
@click.pass_obj
def register(cache: SqliteDict, name: str, key: str, comment: str | None):
    """
    Register a new OTP account.

    NAME: the name of the account to register.
    KEY: the initial key provided by authenticator (no dashes/spaces!)
    """
    if name in cache and not click.confirm(f'Overwrite account "{ name }"?'):
        raise click.Abort()
    token = pyotp.TOTP(key).now()
    pyperclip.copy(token)
    click.echo(f'One-time token "{ token }" for authenticator copied to your clipboard.')
    with cache:
        cache[name] = (key, comment)
        cache.commit()
    # NB: this has no effect in Windows
    cache.filename.chmod(stat.S_IRUSR | stat.S_IWUSR)
    click.echo(f'Account "{ name }" registered.')

@cli.command()
@click.argument('name')
@click.pass_obj
def delete(cache: SqliteDict, name: str):
    """
    Delete a named account.
    """
    if name not in cache:
        raise click.BadParameter(f'unknown account "{ name }".')
    with cache:
        del cache[name]
        cache.commit()
    click.echo(f'Account "{ name }" deleted.')

@cli.command('list')
@click.pass_obj
def list_accounts(cache: SqliteDict):
    """
    List the registered accounts.
    """
    table = [[name, comment] for name, [_, comment] in cache.items()]
    click.echo(tabulate(table, headers=['Account', 'Comment']))

@cli.command()
@click.argument('name')
@click.pass_obj
def totp(cache: SqliteDict, name: str):
    """
    Generate a time-based token for the previously registered account.
    """
    if name not in cache:
        raise click.BadParameter(f'unknown account "{ name }".')
    key, _ = cache[name]
    token = pyotp.TOTP(key).now()
    click.echo(token)
    pyperclip.copy(token)


if __name__ == '__main__':
    cli()
