import { CalendarIcon } from "@chakra-ui/icons";
import { useLocation, useNavigate } from "react-router-dom";
import {
  AccordionButton,
  AccordionIcon,
  AccordionItem,
  AccordionPanel,
  Box,
  Flex,
  Icon,
  Radio,
  RadioGroup,
  Spacer,
  Stack,
} from "@chakra-ui/react";
import { useState } from "react";
import { PiListNumbersThin } from "react-icons/pi";
import { RiMoneyDollarBoxLine } from "react-icons/ri";

export default function ReceiptOrderByMenu() {
  const [dateOrderByRadio, setDateOrderByradio] = useState("1");
  const [moneyOrderByRadio, setMoneyOrderByRadio] = useState("1");
  const accordionMargin = [0, 0, "200px", "500px"];

  const location = useLocation();
  const navigate = useNavigate();
  const queryParams = new URLSearchParams(location.search);
  const updateQueryParamsAndNavigate = (orderBy: string, sort: string) => {
    queryParams.set("orderBy", orderBy);
    queryParams.set("sort", sort);
    const newSearch = queryParams.toString();

    navigate(`/receipts?${newSearch}`);
  };
  return (
    <AccordionItem ml={accordionMargin} mr={accordionMargin}>
      <h2>
        <AccordionButton>
          <Box as="span" flex="1" textAlign="left">
            <Icon as={PiListNumbersThin} />
            &nbsp; Order by
          </Box>
          <AccordionIcon />
        </AccordionButton>
      </h2>
      <AccordionPanel pb={4}>
        <Flex direction={"column"} as="ul" listStyleType={"none"} gap={3}>
          <Flex
            as="li"
            gap="8px"
            justifyContent="space-between"
            alignItems="center"
          >
            <Icon as={CalendarIcon} mr="12px" />
            <RadioGroup onChange={setDateOrderByradio} value={dateOrderByRadio}>
              <Stack direction="row">
                <Radio
                  value="asc"
                  onChange={() => updateQueryParamsAndNavigate("date", "asc")}
                >
                  Ascending
                </Radio>
                <Spacer />
                <Radio
                  value="desc"
                  onChange={() => updateQueryParamsAndNavigate("date", "desc")}
                >
                  Descending
                </Radio>
              </Stack>
            </RadioGroup>
          </Flex>
          <Flex
            as="li"
            gap="4px"
            justifyContent="space-between"
            alignItems="center"
          >
            <Icon as={RiMoneyDollarBoxLine} mr="12px" />
            <RadioGroup
              onChange={setMoneyOrderByRadio}
              value={moneyOrderByRadio}
            >
              <Stack direction="row">
                <Radio
                  value="asc"
                  onChange={() => updateQueryParamsAndNavigate("money", "asc")}
                >
                  Ascending
                </Radio>
                <Spacer />
                <Radio
                  value="desc"
                  onChange={() => updateQueryParamsAndNavigate("money", "desc")}
                >
                  Descending
                </Radio>
              </Stack>
            </RadioGroup>
          </Flex>
        </Flex>
      </AccordionPanel>
    </AccordionItem>
  );
}
