import { ColorModeSwitcher } from "./ColorModeSwitcher";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import NavBar from "./components/navigation/NavBar";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import VerifyEmailPage from "./pages/VerifyEmailPage";
import RequestNewPasswordPage from "./pages/RequestNewPasswordPage";
import RequestNewEmailVerificationPage from "./pages/RequestNewEmailVerificationPage";
import LogoutPage from "./pages/LogoutPage";

export const App = () => {
  return (
    <>
      <Router>
        <NavBar />
        <Routes>
          <Route path="/" element={<HomePage />} />

          <Route path="/auth/login" element={<LoginPage />} />
          <Route path="/auth/register" element={<RegisterPage />} />
          <Route path="/auth/logout" element={<LogoutPage />} />
          <Route path="/auth/verify-email" element={<VerifyEmailPage />} />
          <Route
            path="/auth/request-new-password"
            element={<RequestNewPasswordPage />}
          />
          <Route
            path="/auth/request-new-email-verification"
            element={<RequestNewEmailVerificationPage />}
          />
        </Routes>
      </Router>
    </>
  );
};
