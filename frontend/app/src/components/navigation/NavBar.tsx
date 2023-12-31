import { Button, Flex, HStack, Heading, Link, Text } from "@chakra-ui/react";
import React from "react";
import { Link as NavLink } from "react-router-dom";
import { ColorModeSwitcher } from "../../ColorModeSwitcher";
import NavDesktop from "./NavDesktop";
import NavMobile from "./NavMobile";
import { CopyIcon } from "@chakra-ui/icons";

export type navLinkMapping = {
  name: string;
  route: string;
};

export default function NavBar() {
  const navLinkMappings: navLinkMapping[] = [
    {
      name: "dashboard",
      route: "/dashboard",
    },
    {
      name: "receipts",
      route: "/receipts",
    },
    {
      name: "add receipt",
      route: "/add-receipt",
    },
    {
      name: "exports",
      route: "/exports",
    },
  ];

  return (
    <Flex
      p={[2, 2, 5, 5]}
      justifyContent="space-between"
      alignItems="center"
      boxShadow="base"
    >
      <Heading size="lg">
        <NavLink to="/dashboard">
          <HStack>
            <CopyIcon mr={1} /> <Text>Mijnbonnetje.nl</Text>
          </HStack>
        </NavLink>
      </Heading>
      <NavDesktop links={navLinkMappings} />
      <NavMobile links={navLinkMappings} />
    </Flex>
  );
}
