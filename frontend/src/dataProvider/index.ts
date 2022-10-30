import { stringify } from 'query-string';
import { fetchUtils, DataProvider } from 'ra-core';

function getFromData(params: any) {
    console.log(params);
    const formData = new FormData();
    for (const param in params.data) {
        if (params.data[param]) {
            if (param === 'file') {
                formData.append('file', params.data[param].rawFile);
                continue
            }
            if (param === 'files') {
                params.data[param].forEach((file: any) => {
                    formData.append('files', file.rawFile);
                });
                continue
            }
            formData.append(param, params.data[param]);
        }

    };
    return formData;
}

export default (
    apiUrl: string,
    httpClient = fetchUtils.fetchJson,
    countHeader: string = 'Content-Range'
): DataProvider => ({
    getList: (resource, params) => {
        const { page, perPage } = params.pagination;
        const { field, order } = params.sort;

        const rangeStart = (page - 1) * perPage;
        const rangeEnd = page * perPage - 1;

        const query = {
            sort: JSON.stringify([field, order]),
            range: JSON.stringify([rangeStart, rangeEnd]),
            filter: JSON.stringify(params.filter),
        };
        const url = `${apiUrl}/${resource}?${stringify(query)}`;
        const options =
            countHeader === 'Content-Range'
                ? {
                    // Chrome doesn't return `Content-Range` header if no `Range` is provided in the request.
                    headers: new Headers({
                        Range: `${resource}=${rangeStart}-${rangeEnd}`,
                    }),
                }
                : {};

        return httpClient(url, options).then(({ headers, json }) => {
            if (!headers.has(countHeader)) {
                throw new Error(
                    `The ${countHeader} header is missing in the HTTP Response. The simple REST data provider expects responses for lists of resources to contain this header with the total number of results to build the pagination. If you are using CORS, did you declare ${countHeader} in the Access-Control-Expose-Headers header?`
                );
            }
            return {
                data: json,
                total:
                    countHeader === 'Content-Range'
                        ? parseInt(
                            headers.get('content-range')!.split('/')!.pop()!,
                            10
                        )
                        : parseInt(headers.get(countHeader.toLowerCase())!),
            };
        });
    },

    getOne: (resource, params) =>
        httpClient(`${apiUrl}/${resource}/${params.id}`).then(({ json }) => ({
            data: json,
        })),

    getMany: (resource, params) => {
        const query = {
            filter: JSON.stringify({ id: params.ids }),
        };
        const url = `${apiUrl}/${resource}?${stringify(query)}`;
        return httpClient(url).then(({ json }) => ({ data: json }));
    },

    getManyReference: (resource, params) => {
        const { page, perPage } = params.pagination;
        const { field, order } = params.sort;

        const rangeStart = (page - 1) * perPage;
        const rangeEnd = page * perPage - 1;

        const query = {
            sort: JSON.stringify([field, order]),
            range: JSON.stringify([(page - 1) * perPage, page * perPage - 1]),
            filter: JSON.stringify({
                ...params.filter,
                [params.target]: params.id,
            }),
        };
        const url = `${apiUrl}/${resource}?${stringify(query)}`;
        const options =
            countHeader === 'Content-Range'
                ? {
                    // Chrome doesn't return `Content-Range` header if no `Range` is provided in the request.
                    headers: new Headers({
                        Range: `${resource}=${rangeStart}-${rangeEnd}`,
                    }),
                }
                : {};

        return httpClient(url, options).then(({ headers, json }) => {
            if (!headers.has(countHeader)) {
                throw new Error(
                    `The ${countHeader} header is missing in the HTTP Response. The simple REST data provider expects responses for lists of resources to contain this header with the total number of results to build the pagination. If you are using CORS, did you declare ${countHeader} in the Access-Control-Expose-Headers header?`
                );
            }
            return {
                data: json,
                total:
                    countHeader === 'Content-Range'
                        ? parseInt(
                            headers.get('content-range')!.split('/')!.pop()!,
                            10
                        )
                        : parseInt(headers.get(countHeader.toLowerCase())!),
            };
        });
    },

    update: (resource, params) => {
        switch (resource) {
            case "faces":
            case "face_images":
                return httpClient(`${apiUrl}/${resource}`, {
                    method: 'PUT',
                    body: getFromData(params),
                }).then(({ json }) => ({ data: json }));
            default:
                return httpClient(`${apiUrl}/${resource}`, {
                    method: 'PUT',
                    body: JSON.stringify(params.data),
                }).then(({ json }) => ({ data: json }));
        }
    },

    updateMany: (resource, params) => {
        switch (resource) {
            case "faces":
            case "face_images":
                return Promise.all(
                    params.ids.map(id =>
                        httpClient(`${apiUrl}/${resource}/${id}`, {
                            method: 'PUT',
                            body: getFromData(params),
                        })
                    )
                ).then(responses => ({ data: responses.map(({ json }) => json.id) }))
            default:
                return Promise.all(
                    params.ids.map(id =>
                        httpClient(`${apiUrl}/${resource}/${id}`, {
                            method: 'PUT',
                            body: JSON.stringify(params.data),
                        })
                    )
                ).then(responses => ({ data: responses.map(({ json }) => json.id) }))

        }

    },

    create: (resource, params) => {
        switch (resource) {
            case "faces":
            case "face_images":
                return httpClient(`${apiUrl}/${resource}`, {
                    method: 'POST',
                    body: getFromData(params),
                }).then(({ json }) => ({ data: json }));
            default:
                return httpClient(`${apiUrl}/${resource}`, {
                    method: 'POST',
                    body: JSON.stringify(params.data),
                }).then(({ json }) => ({ data: json }));
        }
    },

    delete: (resource, params) =>
        httpClient(`${apiUrl}/${resource}/${params.id}`, {
            method: 'DELETE',
            headers: new Headers({
                'Content-Type': 'text/plain',
            }),
        }).then(({ json }) => ({ data: json })),

    deleteMany: (resource, params) =>
        Promise.all(
            params.ids.map(id =>
                httpClient(`${apiUrl}/${resource}/${id}`, {
                    method: 'DELETE',
                    headers: new Headers({
                        'Content-Type': 'text/plain',
                    }),
                })
            )
        ).then(responses => ({
            data: responses.map(({ json }) => json.id),
        })),
});