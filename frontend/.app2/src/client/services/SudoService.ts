/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ActiveUpdateActions } from '../models/ActiveUpdateActions';
import type { ApiCallLog } from '../models/ApiCallLog';
import type { LoginHistory } from '../models/LoginHistory';
import type { RefreshToken } from '../models/RefreshToken';
import type { SudoUpdateActions } from '../models/SudoUpdateActions';
import type { TrafficLogwithMetaData } from '../models/TrafficLogwithMetaData';
import type { User } from '../models/User';
import type { UserWithItems } from '../models/UserWithItems';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SudoService {

    /**
     * Read Login Records
     * Retrieves a list of login history records for the specified user.
     * Requires authentication as a sudo user.
     * @param skip
     * @param limit
     * @param userId
     * @param startDate
     * @param endDate
     * @param dateFilter
     * @returns LoginHistory Successful Response
     * @throws ApiError
     */
    public static sudoReadLoginRecords(
        skip?: number,
        limit: number = 1000,
        userId?: (number | string | null),
        startDate?: (string | null),
        endDate?: (string | null),
        dateFilter: string = 'created_at',
    ): CancelablePromise<Array<LoginHistory>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sudo/login-records',
            query: {
                'skip': skip,
                'limit': limit,
                'user_id': userId,
                'start_date': startDate,
                'end_date': endDate,
                'date_filter': dateFilter,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Refresh Tokens
     * Retrieves a list of refresh tokens associated with the provided user.
     * Requires authentication as a sudo user.
     * @param skip
     * @param limit
     * @param userId
     * @param startDate
     * @param endDate
     * @param dateFilter
     * @returns RefreshToken Successful Response
     * @throws ApiError
     */
    public static sudoReadRefreshTokens(
        skip?: number,
        limit: number = 1000,
        userId?: (number | string | null),
        startDate?: (string | null),
        endDate?: (string | null),
        dateFilter: string = 'created_at',
    ): CancelablePromise<Array<RefreshToken>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sudo/refresh-tokens',
            query: {
                'skip': skip,
                'limit': limit,
                'user_id': userId,
                'start_date': startDate,
                'end_date': endDate,
                'date_filter': dateFilter,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Revoke Refresh Tokens From User
     * Revokes refresh tokens for a specific user identified by user ID.
     * Requires authentication as a sudo user.
     * @param userId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static sudoRevokeRefreshTokensFromUser(
        userId: (number | string),
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/sudo/refresh-token/revoke',
            query: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update User Sudo Status
     * Updates the sudo status of a user identified by their ID.
     * Requires authentication as a sudo user.
     * Accepts an action to either assign or revoke sudo privileges.
     *
     * Raises:
     *
     * 400: {detail: "INVALID_ACTION"}
     *
     * 404: {detail: ""USER_NOT_FOUND}
     * @param userId
     * @param action
     * @returns any Successful Response
     * @throws ApiError
     */
    public static sudoUpdateUserSudoStatus(
        userId: (number | string),
        action: SudoUpdateActions,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/sudo/user/update-sudo/{user_id}',
            path: {
                'user_id': userId,
            },
            query: {
                'action': action,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update User Active Status
     * Updates the active status of a user identified by their ID.
     * Requires authentication as a sudo user.
     * Accepts an action to either enable or disable the account.
     *
     * Raises:
     *
     * 400: {detail: "INVALID_ACTION"}
     *
     * 404: {detail: "USER_NOT_FOUND"}
     * @param userId
     * @param action
     * @returns any Successful Response
     * @throws ApiError
     */
    public static sudoUpdateUserActiveStatus(
        userId: (number | string),
        action: ActiveUpdateActions,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/sudo/user/active/{user_id}',
            path: {
                'user_id': userId,
            },
            query: {
                'action': action,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Sudo Read All Users
     * Retrieves a list of all users based on provided parameters.
     * Requires authentication as a sudo user.
     * Useful for viewing user information with sudo privileges.
     * @param skip
     * @param limit
     * @param userId
     * @param startDate
     * @param endDate
     * @param dateFilter
     * @returns User Successful Response
     * @throws ApiError
     */
    public static sudoSudoReadAllUsers(
        skip?: number,
        limit: number = 1000,
        userId?: (number | string | null),
        startDate?: (string | null),
        endDate?: (string | null),
        dateFilter: string = 'created_at',
    ): CancelablePromise<Array<User>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sudo/user',
            query: {
                'skip': skip,
                'limit': limit,
                'user_id': userId,
                'start_date': startDate,
                'end_date': endDate,
                'date_filter': dateFilter,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Sudo Read Specific User
     * Retrieves information about a specific user identified by user ID.
     * Requires authentication as a sudo user.
     *
     * Raises:
     *
     * 404: {detail: "USER_NOT_FOUND"}
     * @param userId
     * @returns UserWithItems Successful Response
     * @throws ApiError
     */
    public static sudoSudoReadSpecificUser(
        userId: (number | string),
    ): CancelablePromise<UserWithItems> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sudo/user/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read All Api Call Logs
     * Retrieves a list of all API call logs.
     * Requires authentication as a sudo user.
     * Useful for viewing API call history.
     * @returns ApiCallLog Successful Response
     * @throws ApiError
     */
    public static sudoReadAllApiCallLogs(): CancelablePromise<Array<ApiCallLog>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sudo/user-api-call-log',
        });
    }

    /**
     * Read Api Call Log From User
     * Retrieves API call logs for a specific user identified by user ID.
     * Requires authentication as a sudo user.
     *
     * Raises:
     *
     * 404: {detail: "LOGS_NOT_FOUND"}
     * @param userId
     * @returns ApiCallLog Successful Response
     * @throws ApiError
     */
    public static sudoReadApiCallLogFromUser(
        userId: number,
    ): CancelablePromise<ApiCallLog> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sudo/user-api-call-log/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Api Traffic
     * @returns TrafficLogwithMetaData Successful Response
     * @throws ApiError
     */
    public static sudoReadApiTraffic(): CancelablePromise<TrafficLogwithMetaData> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sudo/api-traffic',
        });
    }

}
