import { CalendarIcon } from "@chakra-ui/icons";
import {
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Box,
  Button,
  Flex,
  Icon,
  Input,
  Select,
} from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { BsShop } from "react-icons/bs";
import { BiCategoryAlt } from "react-icons/bi";
import { HiOutlineFilter } from "react-icons/hi";
import { Categories, Store } from "../../client";
import { useLocation, useNavigate } from "react-router-dom";

type ReceiptFilterMenuProps = {
  stores: Store[] | null;
};
export default function ReceiptFilterMenu({ stores }: ReceiptFilterMenuProps) {
  const accordionMargin = [0, 0, "200px", "500px"];
  const categories = Object.values(Categories);
  const [filtersAreSet, setFiltersAreSet] = useState(false);
  const [startDate, setStartDate] = useState("2023-01-01");
  const [endDate, setEndDate] = useState("2023-10-01");

  const location = useLocation();
  const navigate = useNavigate();
  const queryParams = new URLSearchParams(location.search);
  const startDateQueryParam = queryParams.get("startDate");

  const updateQueryParamsAndNavigate = (category: string) => {
    setFiltersAreSet(true);
    queryParams.set("category", category);
    const newSearch = queryParams.toString();

    navigate(`/receipts?${newSearch}`);
  };
  const updateShopParams = (shop: string) => {
    setFiltersAreSet(true);
    queryParams.set("shop", shop);
    const newSearch = queryParams.toString();
    navigate(`/receipts?${newSearch}`);
  };
  const updateStartDateParams = (typeOfDate: string, date: string) => {
    setFiltersAreSet(true);
    queryParams.set(typeOfDate, date);
    const newSearch = queryParams.toString();
    navigate(`/receipts?${newSearch}`);
  };

  useEffect(() => {
    if (startDateQueryParam) {
      setFiltersAreSet(true);
    }
  }, []);
  return (
    <AccordionItem ml={accordionMargin} mr={accordionMargin}>
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
          <Flex as="li" gap="4px" justifyContent="center" alignItems="center">
            <Icon as={CalendarIcon} mr="12px" />
            <Input
              type="date"
              onChange={(e) =>
                updateStartDateParams("startDate", e.target.value)
              }
            />
            <Input
              type="date"
              onChange={(e) => updateStartDateParams("endDate", e.target.value)}
            />
          </Flex>
          <Flex as="li" gap="4px" justifyContent="center" alignItems="center">
            <Icon as={BsShop} mr="12px" />
            <Select
              placeholder="select shop"
              onChange={(e) => updateShopParams(e.target.value)}
            >
              {stores?.map((store) => {
                return <option key={store.id}>{store.name}</option>;
              })}
            </Select>
          </Flex>

          <Flex as="li" gap="4px" justifyContent="center" alignItems="center">
            <Icon as={BiCategoryAlt} mr="12px" />
            <Select
              placeholder="select category"
              onChange={(e) => updateQueryParamsAndNavigate(e.target.value)}
            >
              {categories.map((category, i) => {
                return <option key={i}>{category}</option>;
              })}
            </Select>
          </Flex>
          {filtersAreSet && (
            <Button
              onClick={() => {
                setFiltersAreSet(false);
                navigate("/receipts");
              }}
            >
              Remove filters
            </Button>
          )}
        </Flex>
      </AccordionPanel>
    </AccordionItem>
  );
}
