/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type TrafficLog = {
    path: string;
    client: Array<any>;
    server: Array<any>;
    method: string;
    pathParams?: (Record<string, any> | null);
    type_: string;
    httpVersion: string;
    userId?: (number | string | null);
    queryParameters?: (Record<string, any> | null);
    requestDate: string;
};

