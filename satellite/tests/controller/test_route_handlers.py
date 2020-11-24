import json

from copy import deepcopy
from unittest.mock import Mock, patch

from freezegun import freeze_time

from satellite.db import get_session
from satellite.db.models.route import Route
from satellite.schemas.route import RuleEntrySchema

from ..factories import RouteFactory, RuleEntryFactory
from .base import BaseHandlerTestCase


CREATE_ROUTE_REQUEST = {
    'data': {
        'attributes': {
            'destination_override_endpoint': 'https://httpbin.org',
            'protocol': 'http',
            'host_endpoint': '(.*)\\.verygoodproxy\\.com',
            'transport': 'HTTP',
            'source_endpoint': '*',
            'entries': [
                {
                    'targets': [
                        'body'
                    ],
                    'phase': 'REQUEST',
                    'operation': 'REDACT',
                    'id_selector': None,
                    'operations': None,
                    'classifiers': {},
                    'config': {
                        'expression': None,
                        'condition': 'AND',
                        'rules': [
                            {
                                'condition': None,
                                'rules': None,
                                'expression': {
                                    'field': 'PathInfo',
                                    'type': 'string',
                                    'operator': 'equals',
                                    'values': [
                                        '/post'
                                    ]
                                }
                            },
                            {
                                'condition': None,
                                'rules': None,
                                'expression': {
                                    'field': 'ContentType',
                                    'type': 'string',
                                    'operator': 'equals',
                                    'values': [
                                        'application/json'
                                    ]
                                }
                            }
                        ]
                    },
                    'transformer': 'JSON_PATH',
                    'transformer_config': [
                        '$.field1'
                    ],
                    'public_token_generator': 'UUID',
                    'token_manager': 'PERSISTENT'
                }
            ],
            'tags': {
                'name': 'light-slate-grey-population',
                'source': 'vgs-satellite'
            }
        },
        'type': 'rule-chains'
    }
}


@freeze_time('2020-11-11')
class TestRoutesHandler(BaseHandlerTestCase):
    def setUp(self):
        super().setUp()
        session = get_session()
        session.query(Route).delete()
        session.commit()

    def test_get(self):
        RouteFactory(
            id='2c813c5a-be1b-487f-816d-d692aea96852',
            rule_entries_list=[
                RuleEntryFactory(
                    id='8e6d779a-1f57-4b89-8c0b-579d933f783c',
                ),
            ]
        )

        response = self.fetch(self.get_url('/route'))

        self.assertEqual(response.code, 200)
        self.assertMatchSnapshot(json.loads(response.body))

    def test_post(self):
        uuid_patch = patch(
            'satellite.db.models.route.uuid.uuid4',
            lambda: '2c813c5a-be1b-487f-816d-d692aea96852',
        )
        uuid_patch.start()
        self.addCleanup(uuid_patch.stop)

        response = self.fetch(
            self.get_url('/route'),
            method='POST',
            body=json.dumps(CREATE_ROUTE_REQUEST),
        )

        self.assertEqual(response.code, 200, response.body)
        self.assertMatchSnapshot(json.loads(response.body))


@freeze_time('2020-11-11')
class TestRouteHandler(BaseHandlerTestCase):
    def setUp(self):
        super().setUp()
        session = get_session()
        session.query(Route).delete()
        session.commit()

    def test_get(self):
        route = RouteFactory(
            id='2c813c5a-be1b-487f-816d-d692aea96852',
            rule_entries_list=[
                RuleEntryFactory(
                    id='8e6d779a-1f57-4b89-8c0b-579d933f783c',
                ),
            ]
        )

        response = self.fetch(self.get_url(f'/route/{route.id}'))

        self.assertEqual(response.code, 200)
        self.assertMatchSnapshot(json.loads(response.body))

    def test_put(self):
        route = RouteFactory(
            id='2c813c5a-be1b-487f-816d-d692aea96852',
            rule_entries_list=[
                RuleEntryFactory(
                    id='8e6d779a-1f57-4b89-8c0b-579d933f783c',
                    phase='REQUEST',
                ),
                RuleEntryFactory(id='4066ca33-e740-4b48-bbe9-80cb77e971e7'),
            ],
        )

        update_data = {
            'data': {
                'attributes': {
                    'host_endpoint': r'example\.com',
                    'entries': RuleEntrySchema().dump(
                        route.rule_entries_list,
                        many=True,
                    ),
                },
                'type': 'rule-chains',
            }
        }
        update_data['data']['attributes']['entries'][0]['phase'] = 'RESPONSE'

        response = self.fetch(
            self.get_url(f'/route/{route.id}'),
            method='PUT',
            body=json.dumps(update_data),
        )

        self.assertEqual(response.code, 200, response.body)
        self.assertMatchSnapshot(json.loads(response.body))

    def test_put_create_route(self):
        request = deepcopy(CREATE_ROUTE_REQUEST)
        request['data']['attributes']['entries'][0]['id'] = (
            '33c12208-9e4c-439c-a593-d85711fcdec6'
        )

        response = self.fetch(
            self.get_url('/route/725abda7-e67a-45ee-9d81-47deba32b667'),
            method='PUT',
            body=json.dumps(request),
        )

        self.assertEqual(response.code, 200, response.body)
        self.assertMatchSnapshot(json.loads(response.body))

    def test_put_add_filter_to_existing_route(self):
        uuid_patch = patch(
            'satellite.db.models.route.uuid.uuid4',
            Mock(return_value='ae8df099-4e92-404e-b4c9-80abfdac5f8a'),
        )
        uuid_patch.start()
        self.addCleanup(uuid_patch.stop)

        route = RouteFactory(
            id='2c813c5a-be1b-487f-816d-d692aea96852',
            rule_entries_list=[
                RuleEntryFactory(
                    id='8e6d779a-1f57-4b89-8c0b-579d933f783c',
                    phase='REQUEST',
                ),
            ],
        )

        response = self.fetch(
            self.get_url(f'/route/{route.id}'),
            method='PUT',
            body=json.dumps({
                'data': {
                    'attributes': {
                        'entries': [
                            RuleEntrySchema().dump(route.rule_entries_list[0]),
                            {
                                'targets': ['body'],
                                'phase': 'REQUEST',
                                'operation': 'REDACT',
                                'classifiers': {},
                                'config': {
                                    'condition': 'AND',
                                    'rules': [
                                        {
                                            'expression': {
                                                'field': 'PathInfo',
                                                'type': 'string',
                                                'operator': 'equals',
                                                'values': [
                                                    '/put'
                                                ],
                                            },
                                        },
                                        {
                                            'expression': {
                                                'field': 'ContentType',
                                                'type': 'string',
                                                'operator': 'equals',
                                                'values': [
                                                    'application/json'
                                                ],
                                            },
                                        },
                                    ],
                                },
                                'transformer': 'JSON_PATH',
                                'transformer_config': [
                                    '$.field2'
                                ],
                                'public_token_generator': 'UUID',
                                'token_manager': 'PERSISTENT'
                            },
                        ],
                    },
                    'type': 'rule-chains',
                }
            }),
        )

        self.assertEqual(response.code, 200, response.body)
        self.assertMatchSnapshot(json.loads(response.body))

    def test_put_delete_single_filter(self):
        route = RouteFactory(
            id='2c813c5a-be1b-487f-816d-d692aea96852',
            rule_entries_list=[
                RuleEntryFactory(id='8e6d779a-1f57-4b89-8c0b-579d933f783c'),
                RuleEntryFactory(id='4066ca33-e740-4b48-bbe9-80cb77e971e7'),
            ],
        )

        update_data = {
            'data': {
                'attributes': {
                    'entries': [
                        RuleEntrySchema().dump(route.rule_entries_list[0]),
                    ],
                },
                'type': 'rule-chains',
            }
        }

        response = self.fetch(
            self.get_url(f'/route/{route.id}'),
            method='PUT',
            body=json.dumps(update_data),
        )
        response_data = json.loads(response.body)

        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(len(response_data['entries']), 1)
        self.assertEqual(
            response_data['entries'][0]['id'],
            '8e6d779a-1f57-4b89-8c0b-579d933f783c',
        )
        self.assertMatchSnapshot(response_data)

    def test_put_delete_all_filters(self):
        route = RouteFactory(
            id='2c813c5a-be1b-487f-816d-d692aea96852',
            rule_entries_list=[
                RuleEntryFactory(id='8e6d779a-1f57-4b89-8c0b-579d933f783c'),
                RuleEntryFactory(id='4066ca33-e740-4b48-bbe9-80cb77e971e7'),
            ],
        )

        update_data = {
            'data': {
                'attributes': {
                    'entries': [],
                },
                'type': 'rule-chains',
            }
        }

        response = self.fetch(
            self.get_url(f'/route/{route.id}'),
            method='PUT',
            body=json.dumps(update_data),
        )
        response_data = json.loads(response.body)

        self.assertEqual(response.code, 200, response.body)
        self.assertEqual(len(response_data['entries']), 0)
        self.assertMatchSnapshot(response_data)
