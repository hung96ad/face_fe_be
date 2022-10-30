import * as React from 'react';
import { Admin, CustomRoutes, fetchUtils, Resource } from 'react-admin';
import polyglotI18nProvider from 'ra-i18n-polyglot';
import { Route } from 'react-router';

import authProvider from './authProvider';
import { Login, Layout } from './layout';
import { Dashboard } from './dashboard';
import englishMessages from './i18n/en';
import { lightTheme } from './layout/themes';

import Configuration from './configuration/Configuration';
import users from './users';
import restAPI from './dataProvider';
import rooms from './rooms';
import camera from './camera';
import face from './face';
import face_logs from './face_logs';
import face_logs_unknow from './face_logs_unknow';
import { BASE_URL } from './configuration/config';
const httpClient = (url: any, options: any) => {
    if (!options) {
        options = {};
    }
    if (!options.headers) {
        options.headers = new Headers({ Accept: 'application/json' });
    }
    const token = localStorage.getItem('token');
    options.headers.set('Authorization', `Bearer ${token}`);
    return fetchUtils.fetchJson(url, options);
};

const dataProvider = restAPI(BASE_URL + '/api/v1', httpClient);
const i18nProvider = polyglotI18nProvider(locale => {
    if (locale === 'fr') {
        return import('./i18n/fr').then(messages => messages.default);
    }

    // Always fallback on english
    return englishMessages;
}, 'en');

const App = () => {
    return (
        <Admin
            title=""
            dataProvider={dataProvider}
            authProvider={authProvider}
            dashboard={Dashboard}
            loginPage={Login}
            layout={Layout}
            i18nProvider={i18nProvider}
            disableTelemetry
            theme={lightTheme}
        >
            <CustomRoutes>
                <Route path="/configuration" element={<Configuration />} />
            </CustomRoutes>
            <Resource name="users" {...users} />
            {(permissions: 'admin' | 'user') => [
                permissions === 'admin' ? (
                    [
                        <Resource
                            name="users"
                            options={{ label: 'Quản trị người dùng' }}
                            {...users}
                        />,
                        <Resource
                            name="rooms"
                            options={{ label: 'Quản trị thông tin phòng' }}
                            {...rooms}
                        />,
                        <Resource
                            name="cameras"
                            options={{ label: 'Quản trị thông tin camera' }}
                            {...camera}
                        />,
                        <Resource
                            name="faces"
                            options={{ label: 'Quản trị thông tin khuôn mặt' }}
                            {...face}
                        />,
                        <Resource
                            name="face_logs_not_keep_unknow"
                            options={{ label: 'Face logs' }}
                            {...face_logs}
                        />,
                        <Resource
                            name="face_logs_keep_unknow"
                            options={{ label: 'Face logs unknow' }}
                            {...face_logs_unknow}
                        />,]
                ) : null,
            ]}
        </Admin>
    );
};

export default App;
