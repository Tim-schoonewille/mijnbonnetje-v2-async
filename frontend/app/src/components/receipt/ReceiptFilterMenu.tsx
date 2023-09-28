import { CalendarIcon } from "@chakra-ui/icons";
import {
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Box,
  Flex,
  Icon,
  Select,
} from "@chakra-ui/react";
import React from "react";
import { BsShop } from "react-icons/bs";
import { BiCategoryAlt } from "react-icons/bi";
import { HiOutlineFilter } from "react-icons/hi";

export default function ReceiptFilterMenu() {
  return (
<AccordionItem>
          <h2>
            <AccordionButton>
              <Box as="span" flex="1" textAlign="left">
                <Icon as={HiOutlineFilter} />
                &nbsp; Filters
              </Box>
              <AccordionIcon />
            </AccordionButton>
          </h2>
          <AccordionPanel pb={4}>
            <Flex direction={"column"} as="ul" listStyleType={"none"} gap={3}>
              <Flex
                as="li"
                gap="4px"
                justifyContent="center"
                alignItems="center"
              >
                <Icon as={CalendarIcon} mr="12px" />
                <Select placeholder="select date">
                  <option>Some dates</option>
                </Select>
              </Flex>
              <Flex
                as="li"
                gap="4px"
                justifyContent="center"
                alignItems="center"
              >
                <Icon as={BsShop} mr="12px" />
                <Select placeholder="select shop">
                  <option>Some dates</option>
                </Select>
              </Flex>

              <Flex
                as="li"
                gap="4px"
                justifyContent="center"
                alignItems="center"
              >
                <Icon as={BiCategoryAlt} mr="12px" />
                <Select placeholder="select category">
                  <option>Some dates</option>
                </Select>
              </Flex>
            </Flex>
          </AccordionPanel>
        </AccordionItem>
  )
}
