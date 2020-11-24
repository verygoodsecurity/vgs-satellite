# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestRouteHandler::test_put 1'] = {
    'created_at': '2020-11-11T00:00:00',
    'destination_override_endpoint': '*',
    'entries': [
        {
            'classifiers': {
            },
            'config': {
                'condition': 'AND',
                'expression': None,
                'rules': [
                    {
                        'condition': None,
                        'expression': {
                            'field': 'PathInfo',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                '/post'
                            ]
                        },
                        'rules': None
                    },
                    {
                        'condition': None,
                        'expression': {
                            'field': 'ContentType',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                'application/json'
                            ]
                        },
                        'rules': None
                    }
                ]
            },
            'created_at': '2020-11-11T00:00:00',
            'id': '8e6d779a-1f57-4b89-8c0b-579d933f783c',
            'operation': 'REDACT',
            'phase': 'RESPONSE',
            'public_token_generator': 'UUID',
            'targets': 'body',
            'token_manager': 'PERSISTENT',
            'transformer': 'JSON_PATH',
            'transformer_config': [
                '$.foo'
            ]
        },
        {
            'classifiers': {
            },
            'config': {
                'condition': 'AND',
                'expression': None,
                'rules': [
                    {
                        'condition': None,
                        'expression': {
                            'field': 'PathInfo',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                '/post'
                            ]
                        },
                        'rules': None
                    },
                    {
                        'condition': None,
                        'expression': {
                            'field': 'ContentType',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                'application/json'
                            ]
                        },
                        'rules': None
                    }
                ]
            },
            'created_at': '2020-11-11T00:00:00',
            'id': '4066ca33-e740-4b48-bbe9-80cb77e971e7',
            'operation': 'REDACT',
            'phase': 'REQUEST',
            'public_token_generator': 'UUID',
            'targets': 'body',
            'token_manager': 'PERSISTENT',
            'transformer': 'JSON_PATH',
            'transformer_config': [
                '$.foo'
            ]
        }
    ],
    'host_endpoint': 'example\\.com',
    'id': '2c813c5a-be1b-487f-816d-d692aea96852',
    'port': 443,
    'protocol': 'http',
    'source_endpoint': '*',
    'tags': {
        'source': 'vgs-satellite'
    }
}

snapshots['TestRouteHandler::test_put_create_route 1'] = {
    'created_at': '2020-11-11T00:00:00',
    'destination_override_endpoint': 'https://httpbin.org',
    'entries': [
        {
            'classifiers': {
            },
            'config': {
                'condition': 'AND',
                'expression': None,
                'rules': [
                    {
                        'condition': None,
                        'expression': {
                            'field': 'PathInfo',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                '/post'
                            ]
                        },
                        'rules': None
                    },
                    {
                        'condition': None,
                        'expression': {
                            'field': 'ContentType',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                'application/json'
                            ]
                        },
                        'rules': None
                    }
                ]
            },
            'created_at': '2020-11-11T00:00:00',
            'id': '33c12208-9e4c-439c-a593-d85711fcdec6',
            'operation': 'REDACT',
            'phase': 'REQUEST',
            'public_token_generator': 'UUID',
            'targets': [
                'body'
            ],
            'token_manager': 'PERSISTENT',
            'transformer': 'JSON_PATH',
            'transformer_config': [
                '$.field1'
            ]
        }
    ],
    'host_endpoint': '(.*)\\.verygoodproxy\\.com',
    'id': '725abda7-e67a-45ee-9d81-47deba32b667',
    'port': None,
    'protocol': 'http',
    'source_endpoint': '*',
    'tags': {
        'name': 'light-slate-grey-population',
        'source': 'vgs-satellite'
    }
}

snapshots['TestRouteHandler::test_put_add_filter_to_existing_route 1'] = {
    'created_at': '2020-11-11T00:00:00',
    'destination_override_endpoint': '*',
    'entries': [
        {
            'classifiers': {
            },
            'config': {
                'condition': 'AND',
                'expression': None,
                'rules': [
                    {
                        'condition': None,
                        'expression': {
                            'field': 'PathInfo',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                '/post'
                            ]
                        },
                        'rules': None
                    },
                    {
                        'condition': None,
                        'expression': {
                            'field': 'ContentType',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                'application/json'
                            ]
                        },
                        'rules': None
                    }
                ]
            },
            'created_at': '2020-11-11T00:00:00',
            'id': '8e6d779a-1f57-4b89-8c0b-579d933f783c',
            'operation': 'REDACT',
            'phase': 'REQUEST',
            'public_token_generator': 'UUID',
            'targets': 'body',
            'token_manager': 'PERSISTENT',
            'transformer': 'JSON_PATH',
            'transformer_config': [
                '$.foo'
            ]
        },
        {
            'classifiers': {
            },
            'config': {
                'condition': 'AND',
                'rules': [
                    {
                        'expression': {
                            'field': 'PathInfo',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                '/put'
                            ]
                        }
                    },
                    {
                        'expression': {
                            'field': 'ContentType',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                'application/json'
                            ]
                        }
                    }
                ]
            },
            'created_at': '2020-11-11T00:00:00',
            'id': 'ae8df099-4e92-404e-b4c9-80abfdac5f8a',
            'operation': 'REDACT',
            'phase': 'REQUEST',
            'public_token_generator': 'UUID',
            'targets': [
                'body'
            ],
            'token_manager': 'PERSISTENT',
            'transformer': 'JSON_PATH',
            'transformer_config': [
                '$.field2'
            ]
        }
    ],
    'host_endpoint': 'httpbin\\.org',
    'id': '2c813c5a-be1b-487f-816d-d692aea96852',
    'port': 443,
    'protocol': 'http',
    'source_endpoint': '*',
    'tags': {
        'source': 'vgs-satellite'
    }
}

snapshots['TestRouteHandler::test_put_delete_single_filter 1'] = {
    'created_at': '2020-11-11T00:00:00',
    'destination_override_endpoint': '*',
    'entries': [
        {
            'classifiers': {
            },
            'config': {
                'condition': 'AND',
                'expression': None,
                'rules': [
                    {
                        'condition': None,
                        'expression': {
                            'field': 'PathInfo',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                '/post'
                            ]
                        },
                        'rules': None
                    },
                    {
                        'condition': None,
                        'expression': {
                            'field': 'ContentType',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                'application/json'
                            ]
                        },
                        'rules': None
                    }
                ]
            },
            'created_at': '2020-11-11T00:00:00',
            'id': '8e6d779a-1f57-4b89-8c0b-579d933f783c',
            'operation': 'REDACT',
            'phase': 'REQUEST',
            'public_token_generator': 'UUID',
            'targets': 'body',
            'token_manager': 'PERSISTENT',
            'transformer': 'JSON_PATH',
            'transformer_config': [
                '$.foo'
            ]
        }
    ],
    'host_endpoint': 'httpbin\\.org',
    'id': '2c813c5a-be1b-487f-816d-d692aea96852',
    'port': 443,
    'protocol': 'http',
    'source_endpoint': '*',
    'tags': {
        'source': 'vgs-satellite'
    }
}

snapshots['TestRouteHandler::test_put_delete_all_filters 1'] = {
    'created_at': '2020-11-11T00:00:00',
    'destination_override_endpoint': '*',
    'entries': [
    ],
    'host_endpoint': 'httpbin\\.org',
    'id': '2c813c5a-be1b-487f-816d-d692aea96852',
    'port': 443,
    'protocol': 'http',
    'source_endpoint': '*',
    'tags': {
        'source': 'vgs-satellite'
    }
}

snapshots['TestRoutesHandler::test_get 1'] = [
    {
        'created_at': '2020-11-11T00:00:00',
        'destination_override_endpoint': '*',
        'entries': [
            {
                'classifiers': {
                },
                'config': {
                    'condition': 'AND',
                    'expression': None,
                    'rules': [
                        {
                            'condition': None,
                            'expression': {
                                'field': 'PathInfo',
                                'operator': 'equals',
                                'type': 'string',
                                'values': [
                                    '/post'
                                ]
                            },
                            'rules': None
                        },
                        {
                            'condition': None,
                            'expression': {
                                'field': 'ContentType',
                                'operator': 'equals',
                                'type': 'string',
                                'values': [
                                    'application/json'
                                ]
                            },
                            'rules': None
                        }
                    ]
                },
                'created_at': '2020-11-11T00:00:00',
                'id': '8e6d779a-1f57-4b89-8c0b-579d933f783c',
                'operation': 'REDACT',
                'phase': 'REQUEST',
                'public_token_generator': 'UUID',
                'targets': 'body',
                'token_manager': 'PERSISTENT',
                'transformer': 'JSON_PATH',
                'transformer_config': [
                    '$.foo'
                ]
            }
        ],
        'host_endpoint': 'httpbin\\.org',
        'id': '2c813c5a-be1b-487f-816d-d692aea96852',
        'port': 443,
        'protocol': 'http',
        'source_endpoint': '*',
        'tags': {
            'source': 'vgs-satellite'
        }
    }
]

snapshots['TestRoutesHandler::test_post 1'] = {
    'created_at': '2020-11-11T00:00:00',
    'destination_override_endpoint': 'https://httpbin.org',
    'entries': [
        {
            'classifiers': {
            },
            'config': {
                'condition': 'AND',
                'expression': None,
                'rules': [
                    {
                        'condition': None,
                        'expression': {
                            'field': 'PathInfo',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                '/post'
                            ]
                        },
                        'rules': None
                    },
                    {
                        'condition': None,
                        'expression': {
                            'field': 'ContentType',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                'application/json'
                            ]
                        },
                        'rules': None
                    }
                ]
            },
            'created_at': '2020-11-11T00:00:00',
            'id': '2c813c5a-be1b-487f-816d-d692aea96852',
            'operation': 'REDACT',
            'phase': 'REQUEST',
            'public_token_generator': 'UUID',
            'targets': [
                'body'
            ],
            'token_manager': 'PERSISTENT',
            'transformer': 'JSON_PATH',
            'transformer_config': [
                '$.field1'
            ]
        }
    ],
    'host_endpoint': '(.*)\\.verygoodproxy\\.com',
    'id': '2c813c5a-be1b-487f-816d-d692aea96852',
    'port': None,
    'protocol': 'http',
    'source_endpoint': '*',
    'tags': {
        'name': 'light-slate-grey-population',
        'source': 'vgs-satellite'
    }
}

snapshots['TestRouteHandler::test_get 1'] = {
    'created_at': '2020-11-11T00:00:00',
    'destination_override_endpoint': '*',
    'entries': [
        {
            'classifiers': {
            },
            'config': {
                'condition': 'AND',
                'expression': None,
                'rules': [
                    {
                        'condition': None,
                        'expression': {
                            'field': 'PathInfo',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                '/post'
                            ]
                        },
                        'rules': None
                    },
                    {
                        'condition': None,
                        'expression': {
                            'field': 'ContentType',
                            'operator': 'equals',
                            'type': 'string',
                            'values': [
                                'application/json'
                            ]
                        },
                        'rules': None
                    }
                ]
            },
            'created_at': '2020-11-11T00:00:00',
            'id': '8e6d779a-1f57-4b89-8c0b-579d933f783c',
            'operation': 'REDACT',
            'phase': 'REQUEST',
            'public_token_generator': 'UUID',
            'targets': 'body',
            'token_manager': 'PERSISTENT',
            'transformer': 'JSON_PATH',
            'transformer_config': [
                '$.foo'
            ]
        }
    ],
    'host_endpoint': 'httpbin\\.org',
    'id': '2c813c5a-be1b-487f-816d-d692aea96852',
    'port': 443,
    'protocol': 'http',
    'source_endpoint': '*',
    'tags': {
        'source': 'vgs-satellite'
    }
}
