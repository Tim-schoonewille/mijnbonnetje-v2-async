/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { User } from '../models/User';
import type { UserUpdate } from '../models/UserUpdate';
import type { UserUpdatePassword } from '../models/UserUpdatePassword';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class UserService {

    /**
     * Get Self
     * @returns User Successful Response
     * @throws ApiError
     */
    public static userGetSelf(): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/user/self',
        });
    }

    /**
     * Update Self
     * @param requestBody
     * @returns User Successful Response
     * @throws ApiError
     */
    public static userUpdateSelf(
        requestBody: UserUpdate,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/user',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * User Change Password
     * Change user password. (requires fresh token)
     *
     * Raises:
     *
     * 401: {detail: "INVALID_CREDENTIALS"}
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static userUserChangePassword(
        requestBody: UserUpdatePassword,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/user/change/password',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
