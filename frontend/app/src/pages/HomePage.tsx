import { Box, Flex, Heading } from "@chakra-ui/react";
import React from "react";
import RequiresValidToken from "../wrappers/RequiresValidToken";

export default function HomePage() {
  return (
    <RequiresValidToken>
      <Box> Homepage</Box>
    </RequiresValidToken>
  )
}
