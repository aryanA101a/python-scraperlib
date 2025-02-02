""" URI handling module"""

import urllib.parse
from typing import Optional, Union

from zimscraperlib import logger
from zimscraperlib.misc import first


def rebuild_uri(
    uri: urllib.parse.ParseResult,
    scheme: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    hostname: Optional[str] = None,
    port: Optional[Union[str, int]] = None,
    path: Optional[str] = None,
    params: Optional[str] = None,
    query: Optional[str] = None,
    fragment: Optional[str] = None,
    failsafe: bool = False,  # noqa: FBT001, FBT002
) -> urllib.parse.ParseResult:
    """new ParseResult named tuple from uri with requested part updated"""
    try:
        username = first(username, uri.username, "")  # pyright: ignore
        password = first(password, uri.password, "")  # pyright: ignore
        hostname = first(hostname, uri.hostname, "")  # pyright: ignore
        port = first(port, uri.port, "")  # pyright: ignore
        netloc = (
            f"{username}{':' if password else ''}{password}"
            f"{'@' if username or password else ''}{hostname}"
            f"{':' if port else ''}{port}"
        )
        return urllib.parse.urlparse(  # pyright: ignore
            urllib.parse.urlunparse(  # pyright: ignore
                (  # pyright: ignore
                    first(scheme, uri.scheme),
                    netloc,
                    first(path, uri.path),
                    first(params, uri.params),
                    first(query, uri.query),
                    first(fragment, uri.fragment),
                )
            )
        )
    except Exception as exc:
        if failsafe:
            logger.error(
                f"Failed to rebuild "  # lgtm [py/clear-text-logging-sensitive-data]
                f"URI {uri} with scheme={scheme} username={username} "
                f"password={password} hostname={hostname} port={port} path={path} "
                f"params={params} query={query} fragment={fragment} - {exc}"
            )
            return uri
        raise exc
