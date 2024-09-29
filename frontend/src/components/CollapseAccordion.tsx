import {Collapse, Box, Accordion } from '@mantine/core';
import {Appointment} from '../store/patientsSlice';
import React from "react";
import {transformDate} from '../utils';
import card from '../assets/scss/card.module.scss'

interface CollapseProps {
  isOpen: boolean;
  appointments: Appointment[];
}

function CollapseAccordion(props: CollapseProps) {
  const {isOpen, appointments} = props;

  return (
    <Box maw={400} mx="auto">
      <Collapse in={isOpen}>
        <Accordion className={card.accordionBlock}>
          {appointments.map((appointment) => (
            <Accordion.Item key={appointment.id} value={String(appointment.id)}>
              <Accordion.Control>{transformDate(appointment.date_start, true)} {appointment.status}</Accordion.Control>
              <Accordion.Panel>{appointment.description}</Accordion.Panel>
            </Accordion.Item>
            ))}
        </Accordion>
      </Collapse>
    </Box>
  );
}

export default CollapseAccordion;