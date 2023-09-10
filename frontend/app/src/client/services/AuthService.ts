/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RequestNewPassword } from '../models/RequestNewPassword';
import type { Tokens } from '../models/Tokens';
import type { User } from '../models/User';
import type { UserCreate } from '../models/UserCreate';
import type { UserLogin } from '../models/UserLogin';
import type { ValidateRequestNewPassword } from '../models/ValidateRequestNewPassword';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class AuthService {

    /**
     * Register New User
     * Register a new user.
     *
     *
     * Check if the user is already registered.
     *
     * Hash the user's password for security.
     *
     * Create a new user record in the database.
     *
     * Generate an email verification token.
     *
     * Send an email to the user with the verification token.
     *
     *
     * Raises:
     *
     * 400: If the user is already registered. (detail: 'DUPLICATE_EMAIL')
     * @param requestBody
     * @returns User Successful Response
     * @throws ApiError
     */
    public static authRegisterNewUser(
        requestBody: UserCreate,
    ): CancelablePromise<User> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/signup',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Login User
     * Log in a user and return access and refresh tokens.
     *
     * Retrieve the user from the database based on email.
     * Check login attempts and account lock status.
     * Authenticate the user's password.
     * Consume existing refresh tokens.
     * Register the new login and issue new tokens.
     *
     * Raises:
     *
     * 400: invalid credentials: {detail: 'INVALID_CREDENTIALS'}
     *
     * 401: too many login attempts: {detail: 'LOCKED_OUT}
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static authLoginUser(
        requestBody: UserLogin,
    ): CancelablePromise<(User | Record<string, string>)> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/login',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Logout
     * Log out a user and revoke tokens.
     *
     * Revoke refresh tokens associated with the user.
     * Delete access and refresh tokens from cookies.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static authLogout(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/auth/logout',
        });
    }

    /**
     * Verify Token
     * Verify an access token.
     *
     * No additional logic, simply indicate token verification.
     * Raises:
     *
     * 401: {detail: 'TOKENS_EXPIRED'}
     *
     * 401: {detail: 'REFRESH_TOKEN_REVOKED'}
     *
     * 403: {detail: 'EMAIL_NOT_VERIFIED'}
     *
     * 404: {detail: 'INVALID_USER}
     * @returns any Successful Response
     * @throws ApiError
     */
    public static authVerifyToken(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/auth/verify-token',
        });
    }

    /**
     * Verify Fresh Token
     * Verify that token is a fresh token.
     *
     * Raises:
     *
     * 401: {detail: 'TOKENS_EXPIRED'}
     *
     * 401: {detail: 'REFRESH_TOKEN_REVOKED'}
     *
     * 403: {detail: 'EMAIL_NOT_VERIFIED'}
     *
     * 404: {detail: 'INVALID_USER}
     *
     * 401: {detail: 'REQUIRES_FRESH_TOKEN'}
     * @returns boolean Successful Response
     * @throws ApiError
     */
    public static authVerifyFreshToken(): CancelablePromise<Record<string, boolean>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/auth/verify-fresh-token',
        });
    }

    /**
     * Verify Sudo Token
     * Verify user/token has sudo rights.
     *
     * Raises:
     *
     * 401: {detail: 'TOKENS_EXPIRED'}
     *
     * 401: {detail: 'REFRESH_TOKEN_REVOKED'}
     *
     * 403: {detail: 'EMAIL_NOT_VERIFIED'}
     *
     * 404: {detail: 'INVALID_USER}
     *
     * 403: {detail: 'REQUIRES_SUDO'}
     * @returns boolean Successful Response
     * @throws ApiError
     */
    public static authVerifySudoToken(): CancelablePromise<Record<string, boolean>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/auth/verify-sudo-token',
        });
    }

    /**
     * Request Email Verification Code
     * Request a new email verification code.
     *
     * Generate a new email verification token.
     * Send an email to the user with the verification token.
     *
     * Raised:
     *
     * 400: {detail: 'ALREADY_VERIFIED}
     * @returns any Successful Response
     * @throws ApiError
     */
    public static authRequestEmailVerificationCode(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/auth/email/verify/new',
        });
    }

    /**
     * Verify Email
     * Verify a user's email address.
     *
     * Validate the email verification token.
     * Verify the user's email address in the database.
     *
     * Raises:
     *
     * 400: {detail: 'INVALID_TOKEN}
     *
     * 404: {detail: "USER_NOT_FOUND"}
     * @param token
     * @returns any Successful Response
     * @throws ApiError
     */
    public static authVerifyEmail(
        token: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/auth/email/verify/',
            query: {
                'token': token,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Request New Password Token
     * Request a new password reset token.
     *
     * Check if the email exists in the database.
     * Generate a new password reset token.
     *
     * Raises:
     *
     * 404: {detail: 'INVALID_EMAIL'}
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static authRequestNewPasswordToken(
        requestBody: RequestNewPassword,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/password/reset',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Verify New Password Request
     * Verify a new password reset request.
     *
     * Validate the password reset token.
     * Update the user's password in the database.
     *
     * Raises:
     *
     * 401: {detail: 'INVALID_OR_EXPIRED_TOKEN'}
     *
     * 400: {detail: 'INVALID_TOKEN_SUB'}
     * @param token
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static authVerifyNewPasswordRequest(
        token: string,
        requestBody: ValidateRequestNewPassword,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/auth/password/reset/verify',
            query: {
                'token': token,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Handle Two Factor Otp
     * Verify two factor OTP
     *
     * Raises:
     *
     * 401: {detail: 'INVALID_OTP}
     *
     * 404: {detail: 'USER_NOT_FOUND'}
     * @param otpSessionId
     * @param otp
     * @returns Tokens Successful Response
     * @throws ApiError
     */
    public static authHandleTwoFactorOtp(
        otpSessionId: string,
        otp: string,
    ): CancelablePromise<Tokens> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/auth/twofactor/',
            query: {
                'otp_session_id': otpSessionId,
                'otp': otp,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Two Factor Authentication
     * Enable or disable two factor authentication.
     * @param action
     * @returns any Successful Response
     * @throws ApiError
     */
    public static authUpdateTwoFactorAuthentication(
        action: boolean,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/auth/twofactor/enable/{action}',
            path: {
                'action': action,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Twofactor Renew
     * Request a new OTP for two factor authentication.
     *
     * Raises:
     *
     * 400: {detail: 'INVALID_SESSION_ID}
     * @param otpSessionId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static authTwofactorRenew(
        otpSessionId: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/auth/twofactor/renew',
            query: {
                'otp_session_id': otpSessionId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
