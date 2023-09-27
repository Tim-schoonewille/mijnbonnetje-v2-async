/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Subscription } from '../models/Subscription';
import type { SubscriptionCreateSchema } from '../models/SubscriptionCreateSchema';
import type { SubscriptionUpdate } from '../models/SubscriptionUpdate';
import type { SubscriptionWithTier } from '../models/SubscriptionWithTier';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SubscriptionService {

    /**
     * Read All Active Subscriptions
     * Return all subscriptions
     * @param skip
     * @param limit
     * @param userId
     * @param startDate
     * @param endDate
     * @param dateFilter
     * @returns any Successful Response
     * @throws ApiError
     */
    public static subscriptionReadAllActiveSubscriptions(
        skip?: number,
        limit: number = 1000,
        userId?: (number | string | null),
        startDate?: (string | null),
        endDate?: (string | null),
        dateFilter: string = 'created_at',
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sub/subscription/',
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
     * Create New Subscription
     * Create a new subscription.
     *
     * Raises:
     *
     * 402: {detail: "PAYMENT_PENDING_FOR_SUB"}
     *
     * 404: {detail: "TIER_NOT_FOUND"}
     *
     * 409: {detail: "ALREADY_SUBBED"}
     * @param requestBody
     * @returns SubscriptionWithTier Successful Response
     * @throws ApiError
     */
    public static subscriptionCreateNewSubscription(
        requestBody: SubscriptionCreateSchema,
    ): CancelablePromise<SubscriptionWithTier> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/sub/subscription/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Specific Subscription
     * Returns a specific subscription based on ID
     *
     * Raises:
     *
     * 403: {detail: 'NOT_YOUR_SUBSCRIPTION'}
     *
     * 404: {detail: 'SUBSCRIPTION_NOT_FOUND'}
     * @param subscriptionId
     * @returns SubscriptionWithTier Successful Response
     * @throws ApiError
     */
    public static subscriptionReadSpecificSubscription(
        subscriptionId: (number | string),
    ): CancelablePromise<SubscriptionWithTier> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sub/subscription/{subscription_id}',
            path: {
                'subscription_id': subscriptionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Subscription
     * Update subscription (requires sudo)
     *
     * Raises:
     *
     * 403: {detail: "NOT_YOUR_SUBSCRIPTION"}
     *
     * 404: {detail: "SUBSCRIPTION_NOT_FOUND"}
     * @param subscriptionId
     * @param requestBody
     * @returns Subscription Successful Response
     * @throws ApiError
     */
    public static subscriptionUpdateSubscription(
        subscriptionId: (number | string),
        requestBody: SubscriptionUpdate,
    ): CancelablePromise<Subscription> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/sub/subscription/{subscription_id}',
            path: {
                'subscription_id': subscriptionId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Subscription
     * Delete subscription (requires sudo)
     *
     * Raises:
     *
     * 404: {detail: "SUBSCRIPTION_NOT_FOUND"}
     * @param subscriptionId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static subscriptionDeleteSubscription(
        subscriptionId: (number | string),
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/sub/subscription/{subscription_id}',
            path: {
                'subscription_id': subscriptionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
