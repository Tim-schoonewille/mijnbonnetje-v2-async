/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class HealthCheckService {

    /**
     * Pong
     * @returns any Successful Response
     * @throws ApiError
     */
    public static healthCheckPong(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/health/ping',
        });
    }

}
