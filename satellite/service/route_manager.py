from typing import List

from ..db import get_session, update_model
from ..db.models.route import Route, RuleEntry, RouteType


class EntityNotFound(Exception):
    pass


def get_all() -> List[Route]:
    return get_session().query(Route).all()


def get_all_by_type(route_type: RouteType) -> List[Route]:
    route_all = get_all()
    if route_type == RouteType.OUTBOUND:
        return [route for route in route_all if route.is_outbound()]
    else:
        return [route for route in route_all if not route.is_outbound()]


def get(route_id: str) -> Route:
    return get_session().query(Route).filter(Route.id == route_id).first()


def create(route_data: dict) -> Route:
    route = Route(**{
        **route_data,
        'rule_entries_list': [
            RuleEntry(**rule_entry)
            for rule_entry in route_data.get('rule_entries_list', [])
        ]
    })

    session = get_session()
    try:
        session.add(route)
        session.commit()
    except Exception:
        session.rollback()
        raise

    return route


def update(route_id: str, route_data: dict) -> Route:
    route = get(route_id)
    if not route:
        # Have to allow route creation via update since currently FE uses the
        # update endpoint for routes import.
        return create({**route_data, 'id': route_id})

    update_model(route, route_data)

    session = get_session()

    # Do filters CRUD only if they are mentioned in the request
    if 'rule_entries_list' in route_data:
        current_filters = {entry.id: entry for entry in route.rule_entries_list}
        target_filters = []
        target_filters_ids = set()
        filters_data = route_data['rule_entries_list'] or []
        for filter_data in filters_data:
            filter = None
            filter_id = filter_data.get('id')
            if filter_id is not None:
                filter = current_filters.get(filter_id)
            if filter:
                update_model(filter, filter_data, ['id'])
            else:
                filter = RuleEntry(**filter_data)
            target_filters.append(filter)
            target_filters_ids.add(filter.id)

        for filter in route.rule_entries_list:
            if filter.id not in target_filters_ids:
                session.delete(filter)

        route.rule_entries_list = target_filters

    try:
        session.commit()
    except Exception:
        session.rollback()
        raise

    return route


def delete(route_id):
    route = get(route_id)
    session = get_session()
    session.delete(route)
    session.commit()
