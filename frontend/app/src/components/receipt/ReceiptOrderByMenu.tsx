import { CalendarIcon } from "@chakra-ui/icons";
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
  Select,
  Spacer,
  Stack,
} from "@chakra-ui/react";
import { useState } from "react";
import { PiListNumbersThin } from "react-icons/pi";
import { RiMoneyDollarBoxLine } from "react-icons/ri";

export default function ReceiptOrderByMenu() {
  const [dateOrderByRadio, setDateOrderByradio] = useState("1");
  const [moneyOrderByRadio, setMoneyOrderByRadio] = useState("1");
  return (
    <AccordionItem>
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
                <Radio value="asc">Ascending</Radio>
                <Spacer />
                <Radio value="desc">Descending</Radio>
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
            <RadioGroup onChange={setMoneyOrderByRadio} value={moneyOrderByRadio}>
              <Stack direction="row">
                <Radio value="asc">Ascending</Radio>
                <Spacer />
                <Radio value="desc">Descending</Radio>
              </Stack>
            </RadioGroup>
          </Flex>
        </Flex>
      </AccordionPanel>
    </AccordionItem>
  );
}
