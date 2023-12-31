import React, { Dispatch, ReactNode, SetStateAction, useContext, useEffect } from "react";
import { createContext, useState } from "react";
import { AuthService } from "../client";

export interface AuthContextInterface {
  isLoggedIn: boolean;
  setIsLoggedIn: Dispatch<SetStateAction<boolean>>;
  tokenIsVerified: boolean;
  setTokenIsVerified: Dispatch<SetStateAction<boolean>>;
}

// export const AuthContext = createContext<Partial<AuthContextInterface>>({});
export const AuthContext = createContext(null as any as AuthContextInterface);

type AuthProviderProps = {
  children: ReactNode;
};

export default function AuthProvider({ children }: AuthProviderProps) {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [tokenIsVerified, setTokenIsVerified] = useState(false);



  return (
    <AuthContext.Provider
      value={{ isLoggedIn, setIsLoggedIn, tokenIsVerified, setTokenIsVerified }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuthContext = () => useContext(AuthContext);
