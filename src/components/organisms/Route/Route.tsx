import React, { useState } from 'react';
import InboundHosts from 'src/components/organisms/RouteHosts/InboundHosts';
import OutboundHosts from 'src/components/organisms/RouteHosts/OutboundHosts';
import Yaml from 'src/components/molecules/Yaml/Yaml';
import RouteEntry from 'src/components/organisms/RouteEntry/RouteEntry';
import RouteEntrySummary from 'src/components/organisms/RouteEntry/RouteEntrySummary';
import { getEntryTemplate } from 'src/data/routes';
import { isInbound } from 'src/redux/utils/routes';
import RouteName from 'src/components/organisms/RouteName/RouteName';
import DocsPopover from 'src/components/organisms/DocsPopover/DocsPopover';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';
import { Card, CardHeader, CardBody, Collapse } from 'reactstrap';
import classNames from 'classnames';
import { Button, Icon, Popover } from 'src/components/antd';
import RouteNavigationModal from 'src/components/organisms/RouteNavigationModal/RouteNavigationModal';
import { cloneDeep, uniqueId } from 'lodash';
import { IRoute, IEntry } from 'src/redux/interfaces/routes';

export interface IInboundRouteProps {
  route: IRoute;
  routes: IRoute[];
  onChange: (route: IRoute) => void;
}

export const Route: React.FC<IInboundRouteProps> = (props) => {
  const {
    route,
    routes,
  } = props;

  const isEdit = Boolean(route.id);
  const isRouteInbound = isInbound(route);
  const [isCollapse, setIsCollapse] = useState(true);
  const [status, setStatus] = useState('unordered-list');
  const [activeItem, setActiveItem] = useState(-1);

  const onChange = (change) => {
    const updatedRoute = { ...route, ...change };
    props.onChange(updatedRoute);
  };

  const onChangeEntry = (key: number, entry: IEntry) => {
    const entries = [...route.entries];
    entries[key] = entry;
    props.onChange({
      ...route,
      ...{
        entries,
      },
    });
  };

  const addEntry = () => {
    props.onChange({ ...route,
      entries: [...route.entries, getEntryTemplate(isRouteInbound)],
    });
  };

  const removeEntry = (entries: IEntry[]) => {
    // remove entry from route
    props.onChange({
      ...route,
      entries,
    });
  };

  const onRevertEntry = (idx: number, state: boolean) => {
    const entries = cloneDeep(route.entries);
    setActiveItem(idx);
    setTimeout(() => {
      entries[idx].removing = state;
      removeEntry(entries);
      setActiveItem(-1);
    },         state ? 700 : 0);
  };

  const duplicateEntry = (entry: IEntry) => {
    const duplicatedEntry = { ...entry, filter_id: uniqueId() };
    delete duplicatedEntry.id;
    props.onChange({ ...route,
      entries: [...route.entries, duplicatedEntry],
    });
  };

  const getEntryStyle = (isDragging, draggableStyle) => ({
    userSelect: 'none',
    marginBottom: '1rem',
    // styles we need to apply on draggables
    ...draggableStyle,
  });

  const reorder = (list: IEntry[], startIndex: number, endIndex: number) => {
    const result = Array.from(list);
    const [removed] = result.splice(startIndex, 1);
    result.splice(endIndex, 0, removed);

    return result;
  };

  const onDragEnd = (result: any) => {
    // dropped outside the list
    if (!result.destination) {
      return;
    }

    const entries = reorder(
      route.entries,
      result.source.index,
      result.destination.index,
    );

    props.onChange({
      ...route,
      entries,
    });
  };

  const getEntryHeader = (entry: IEntry, idx: number): JSX.Element => {
    return (
      <div
        className={classNames(
          { removing: activeItem === idx },
          'd-flex justify-content-between align-items-center progress-filter',
        )}
      >
        <RouteEntrySummary entry={entry} />
        <div className="d-flex ml-3">
          {!entry.removing &&
          <Popover
            placement="top"
            content="Duplicate Filter"
          >
            <Button
              type="link"
              data-role="edit-route-duplicate-filter-button"
              onClick={() => duplicateEntry(entry)}
            >
              <Icon
                type="copy"
                className="text-primary-light"
              />
            </Button>
          </Popover>
          }
          <Button
            type={entry.removing ? 'dark' : 'link'}
            data-role={`edit-route-${entry.removing ? 'revert' : 'delete' }-filter-button`}
            ghost={entry.removing}
            className="ml-auto"
            onClick={() => onRevertEntry(idx, !entry.removing)}
          >
            <Icon
              type={entry.removing ? 'undo' : 'close'}
              className={classNames({
                'text-primary-light': !entry.removing,
              })}
            />
            {entry.removing && 'Revert'}
          </Button>
        </div>
      </div>
    );
  };

  return (
    <>
      <div>
        {isEdit &&
          <Yaml route={route} />
        }
        <h2>
          {isRouteInbound ? 'Inbound' : 'Outbound'} Route
          <p className="small text-muted">{route.id}</p>
        </h2>
      </div>

      <RouteNavigationModal
        route={route}
        title="You have some unsaved changes"
        content="Do you want to leave the route page?"
      />

      <div className="mb-3 card">
        <div className="card-header">
          <div>
          <span className="mr-1" data-role="edit-route-card-header">
            {!!route.id
              ? `Edit ${isRouteInbound ? 'inbound' : 'outbound'} route`
              : `Add an ${isRouteInbound ? 'inbound' : 'outbound'} route`
            }
          </span>
            <DocsPopover term={`${isRouteInbound ? 'inbound' : 'outbound'} connection`}/>
          </div>
        </div>
        <div  className="card-body">

          <RouteName
            route={route}
            onChangeRouteName={onChange}
            isCreate={!isEdit}
          />
          {isRouteInbound ?
            <InboundHosts
              route={route}
              isEditMode={!!route.id}
              onChangeHost={onChange}
              routes={routes}
              cnames={[]}
            />
          :
            <OutboundHosts
              route={route}
              isEditMode={!!route.id}
              onChangeHost={onChange}
            />
          }
        </div>
      </div>

      {route.entries &&
        <h3>Filters</h3>
      }
      {(route.entries.length > 1 || route.entries.length === 1 && !isCollapse) &&
        <Button
          color="dark"
          onClick={() => setIsCollapse(!isCollapse)}
          className="mb-3"
        >
          <Icon
            type={status}
          />
          {isCollapse ? 'Reorder' : 'Done'}
        </Button>
      }

      <DragDropContext onDragEnd={onDragEnd}>
        <Droppable droppableId="droppable" data-role="filter-list">
          {provide => (
            <div
              {...provide.droppableProps}
              ref={provide.innerRef}
            >
              {route.entries.map((entry, index) => (
                <Draggable
                  key={entry.id || entry.filter_id}
                  draggableId={entry.id || entry.filter_id}
                  index={index}
                  isDragDisabled={isCollapse}
                >
                  {(provided, snapshot) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.draggableProps}
                      {...provided.dragHandleProps}
                      style={getEntryStyle(
                        snapshot.isDragging,
                        provided.draggableProps.style,
                      )}
                    >
                      <Card className="mb-3">
                        <CardHeader
                          className={classNames({
                            rounded: !isCollapse},
                          )}
                        >
                          {getEntryHeader(entry, index)}
                        </CardHeader>
                        <Collapse
                          isOpen={isCollapse}
                          onEntering={() => setStatus('loading')}
                          onExiting={() => setStatus('loading')}
                          onEntered={() => setStatus('unordered-list')}
                          onExited={() => setStatus('check')}
                        >
                          {!entry.removing &&
                            <CardBody>
                              <RouteEntry
                                entry={entry}
                                onChange={(routeEntry: IEntry) => onChangeEntry(index, routeEntry)}
                              />
                            </CardBody>
                          }
                        </Collapse>
                      </Card>
                    </div>
                  )}
                </Draggable>
              ))}
              {provide.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>

      <div className="text-center">
        <Button
          ghost
          color="dark"
          data-role="edit-route-add-filter-button"
          onClick={addEntry}
        >
          Add filter
        </Button>
      </div>
      <hr/>
    </>
  );
};

export default Route;
