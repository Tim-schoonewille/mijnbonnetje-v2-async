import React from "react";
import RequiresValidToken from "./wrappers/RequiresValidToken";

const Home = () => {
  return (
    <RequiresValidToken>
      <div>Home</div>
    </RequiresValidToken>
  );
};

export default Home;
