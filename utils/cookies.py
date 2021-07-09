#!/usr/bin/env python
# -*- coding: utf-8 -*-


# from requests import Session
from http.cookiejar import Cookie
# from http.cookiejar import CookieJar
from requests.cookies import RequestsCookieJar as CookieJar
from typing import List, Optional, Dict


def create_cookie(name, value, **kwargs):
    """Make a cookie from underspecified parameters.

    By default, the pair of `name` and `value` will be set for the domain ''
    and sent on every request (this is sometimes called a "super cookie").
    """
    result = {
        'version': kwargs.get('Version', None) or kwargs.get('version', 0),
        'name': name,
        'value': value,
        'port': kwargs.get('Port', None) or kwargs.get('port', None),
        'domain': kwargs.get('Domain', None) or kwargs.get('domain', ''),
        # 'domain': '',
        'path': kwargs.get('Path', None) or kwargs.get('path', '/'),
        'secure': kwargs.get('Secure', None) or kwargs.get('secure', False),
        # 'expires': kwargs.get('expirationDate', None) or kwargs.get('Expires', None) or kwargs.get('expires', None),
        'expires': None,
        'discard': True,
        'comment': None,
        'comment_url': None,
        'rest': {
            'HttpOnly': kwargs.get(
                'HttpOnly',
                None
            ) or kwargs.get(
                'httpOnly',
                None
            ) or kwargs.get(
                'httponly',
                None
            ) or kwargs.get(
                'http_only',
                None
            )
        },
        'rfc2109': False,
    }

    # result.update(kwargs)
    result['port_specified'] = bool(result['port'])
    result['domain_specified'] = bool(result['domain'])
    result['domain_initial_dot'] = result['domain'].startswith('.')
    result['path_specified'] = bool(result['path'])

    return Cookie(**result)


def cookiejar_from_list(cookie_list: List[Optional[Dict]], cookiejar=None):
    """Returns a CookieJar from a key/value dictionary.

    :param cookie_list: Dict of key/values to insert into CookieJar.
    :param cookiejar: (optional) A cookiejar to add the cookies to.
    :rtype: CookieJar
    """
    if cookiejar is None:
        cookiejar = CookieJar()

    if cookie_list is not None:
        for cookie in cookie_list:
            name = cookie.get('name')
            value = cookie.get('value')
            if name and value:
                cookiejar.set_cookie(create_cookie(**cookie))

    return cookiejar
