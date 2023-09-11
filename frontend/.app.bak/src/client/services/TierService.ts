/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Tier } from '../models/Tier';
import type { TierCreate } from '../models/TierCreate';
import type { TierUpdate } from '../models/TierUpdate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class TierService {

    /**
     * Read All Tiers
     * Returns all subscription tiers (requires verified token)
     * @param skip
     * @param limit
     * @param userId
     * @param startDate
     * @param endDate
     * @param dateFilter
     * @returns Tier Successful Response
     * @throws ApiError
     */
    public static tierReadAllTiers(
        skip?: number,
        limit: number = 1000,
        userId?: (number | string | null),
        startDate?: (string | null),
        endDate?: (string | null),
        dateFilter: string = 'created_at',
    ): CancelablePromise<Array<Tier>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sub/tier/',
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
     * Create New Tier
     * Create a new Tier (requires sudo token)
     * @param requestBody
     * @returns Tier Successful Response
     * @throws ApiError
     */
    public static tierCreateNewTier(
        requestBody: TierCreate,
    ): CancelablePromise<Tier> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/sub/tier/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Specific Tier
     * Return specific tier information. (requires verified token)
     *
     * Raises:
     *
     * 404: {detail: "TIER_NOT_FOUND"}
     * @param tierId
     * @returns Tier Successful Response
     * @throws ApiError
     */
    public static tierReadSpecificTier(
        tierId: (number | string),
    ): CancelablePromise<Tier> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sub/tier/{tier_id}',
            path: {
                'tier_id': tierId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Tier
     * Update tier information. (requires sudo token)
     *
     * Raises:
     *
     * 404: {detail: "TIER_NOT_FOUND"}
     * @param tierId
     * @param requestBody
     * @returns Tier Successful Response
     * @throws ApiError
     */
    public static tierUpdateTier(
        tierId: (number | string),
        requestBody: TierUpdate,
    ): CancelablePromise<Tier> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/sub/tier/{tier_id}',
            path: {
                'tier_id': tierId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Tier
     * Delete specific tier. (requires sudo token)
     *
     * Raises:
     *
     * 404: {detail: "TIER_NOT_FOUND"}
     * @param tierId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static tierDeleteTier(
        tierId: (number | string),
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/sub/tier/{tier_id}',
            path: {
                'tier_id': tierId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
