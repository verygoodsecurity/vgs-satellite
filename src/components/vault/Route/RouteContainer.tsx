import React, { useEffect } from 'react';
import { connect } from 'react-redux';
import history from 'src/redux/utils/history';
import RoutePage from 'src/components/organisms/Route/RoutePage';
import { cloneDeep, remove } from 'lodash';
import { Icon } from 'src/components/antd';
import { notify } from 'src/redux/utils/notifications';
import { removeCharset } from 'src/redux/utils/utils';
import { fetchRoutes, deleteRoute, updateCurrentRoute, updateRoute, saveRoute } from 'src/redux/modules/routes';
import { IRoute } from 'src/redux/interfaces/routes';

const mapStateToProps = ({ routes }: any) => {
  return {
    routes: routes.list,
    isLoading: routes.isLoading,
    currentRoute: routes.currentRoute,
  };
}

const mapDispatchToProps = {
  fetchRoutes,
  deleteRoute,
  updateRoute,
  saveRoute,
  updateCurrentRoute,
};

interface IRouteContainerProps {
  routeId: string;
  routes: IRoute[];
  isLoading: boolean;
  currentRoute: IRoute | null;
  fetchRoutes: () => void;
  deleteRoute: (routeId: string) => void;
  updateRoute: (route: IRoute) => void;
  saveRoute: (route: IRoute, params?: any) => void;
  updateCurrentRoute: (route: IRoute | null) => void;
}

const RouteContainer: React.FunctionComponent<IRouteContainerProps> = (props) => {
  const { routeId, routes, isLoading, currentRoute } = props;
  const { fetchRoutes, deleteRoute, updateRoute, updateCurrentRoute, saveRoute } = props;

  useEffect(() => {
    if (!routes.length) {
      fetchRoutes();
    } else if (routeId) {
      const route = routes.find(r => r.id === routeId);
      if (route) {
        updateCurrentRoute(route);
      } else {
        history.push('/routes');
      }
    }
  }, [routes.length])

  const handleCancel = () => history.push('/routes');

  const routeChangeHandler = (r: IRoute | null) => {
    updateCurrentRoute(r);
  }

  const routeSaveHandler = (r: IRoute) => {
    let entries = cloneDeep(r.entries);
    remove(entries, entry => entry.removing === true);
    entries = entries.map(entry => removeCharset('Default', entry));
    try {
      if (routeId) {
        updateRoute({ ...r, entries });
        updateCurrentRoute({ ...r, entries });
      } else {
        saveRoute(
          { ...r, entries },
          {
            cb: () => {
              history.push('/routes');
            },
            source: 'vgs-satellite',
          },
        );
      }
    } catch (error) {
      notify.error(error.message);
    }
  }

  const routeDeleteHandler = (id: string) => {
    deleteRoute(id);
    history.push('/routes');
  }

  return (
    <>
      {!currentRoute ? (
        <div className="text-center my-4">
          <Icon type="loading" />
        </div>
      ) : (
        <RoutePage
          key={currentRoute.id}
          route={currentRoute}
          routes={routes}
          routeSaveHandler={(r: IRoute) => routeSaveHandler(r)}
          routeChangeHandler={(r: IRoute) => routeChangeHandler(r)}
          routeDeleteHandler={(id: string) => routeDeleteHandler(id)}
          handleCancel={() => handleCancel()}
        />
      )}
    </>
  );
};

export default connect(mapStateToProps, mapDispatchToProps)(RouteContainer);
