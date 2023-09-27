import { Button, Flex, useDisclosure, Link } from "@chakra-ui/react";
import React, { useRef } from "react";
import { ColorModeSwitcher } from "../../ColorModeSwitcher";
import { HamburgerIcon } from "@chakra-ui/icons";
import { Link as NavLink } from "react-router-dom";

import {
  Drawer,
  DrawerBody,
  DrawerFooter,
  DrawerHeader,
  DrawerOverlay,
  DrawerContent,
  DrawerCloseButton,
} from "@chakra-ui/react";
import { navLinkMapping } from "./NavBar";

type NavMobileProps = {
  links: navLinkMapping[];
};
export default function NavMobile({ links }: NavMobileProps) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  return (
    <Flex
      display={["flex", "flex", "none", "none"]}
      alignItems="center"
      justifyContent="space-between"
      gap={10}
      pr={5}
    >
      <ColorModeSwitcher justifySelf="flex-end" />
      <Button onClick={onOpen}>
        <HamburgerIcon />
      </Button>

      <Drawer isOpen={isOpen} placement="top" onClose={onClose}>
        <DrawerOverlay />
        <DrawerContent>
          <DrawerCloseButton />
          <DrawerHeader m="0 auto" pr={19}>
            <Flex gap={5}>
              <Button w="auto">Login</Button> <Button>Signup</Button>
            </Flex>
          </DrawerHeader>

          <DrawerBody>
            <Flex as="ul" flexDirection={"column"} listStyleType="none">
              {links.map((navlink) => {
                return (
                  <Link as="li">
                    <NavLink to={navlink.route}>{navlink.name}</NavLink>
                  </Link>
                );
              })}
            </Flex>
          </DrawerBody>

          <DrawerFooter>
            {/* <Button variant="outline" mr={3} onClick={onClose}>
              Cancel
            </Button> */}
            <Button onClick={onClose}>Close</Button>
          </DrawerFooter>
        </DrawerContent>
      </Drawer>
    </Flex>
  );
}
