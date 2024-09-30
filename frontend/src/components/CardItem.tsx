import React, {useState, useEffect} from 'react';
import {Card, Text, Box, Button, Avatar, Badge, Space} from '@mantine/core';
import card from '../assets/scss/card.module.scss';
import {Patient} from '../store/patientsSlice';
import CollapseAccordion from './CollapseAccordion';
import {transformDate} from '../utils';

interface CardProps {
  mainCss: string;
  data: Patient;
  isOpen: boolean;
  onToggle: () => void;
}

function CardItem(props: CardProps) {
  const {mainCss, data, isOpen, onToggle} = props;

  const [displayCss, setDisplayCss] = useState<string>('close')

  useEffect(() => {
    if (!isOpen) {
      setTimeout(() => {
        setDisplayCss('close')
      }, 200)
      return
    }
    setDisplayCss('open')
  }, [isOpen])

  return (
    <Card className={`${card[mainCss]} ${card[displayCss]}`} shadow="sm" padding="lg" radius="md" withBorder>
      <Card.Section className={card.avatarBlock}>
        <Avatar className={card.avatar} variant="light" radius="md" size="xl" src=""/>
      </Card.Section>

      <Box w={200}>
        <Text fw={500} truncate="end" title={data.fullname}>{data.fullname}</Text>
      </Box>

      <div className={card.infoPatient}>
        <div className={card.infoPatientItem}>
          <Text size="sm" fw={500}>
            Пол:
          </Text>
          <Text size="sm">
            {data.gender}
          </Text>
        </div>
        <div className={card.infoPatientItem}>
          <Text size="sm" fw={500}>
            Дата рождения:
          </Text>
          <Text size="sm">
            {transformDate(data.birth_date)}
          </Text>
        </div>
      </div>

      {data.appointments.length && (<><Button className={card.btnAppointment} color="blue" fullWidth mt="md" radius="md"
                                              onClick={onToggle}>
        Записи к врачам
        <Badge className={card.countAppointment} size="xs" circle color='green'>
          {data.appointments.length}
        </Badge>
      </Button><CollapseAccordion isOpen={isOpen} appointments={data.appointments}/></>)
      }
      {!data.appointments.length && <><Space h='xs'/><Text size="sm" ta='center' c='grey'>Записей к врачу нет</Text></>}
    </Card>
  );
}

export default CardItem