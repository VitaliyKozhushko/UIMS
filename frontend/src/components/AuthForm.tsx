import {
  Paper,
  PaperProps,
  Button,
  Divider,
} from '@mantine/core';
import authImg from '../assets/img/images/auth_card.png'
import { useNavigate } from "react-router-dom";

interface CustomProps {
  css: string;
  cssimg: string
}

type AuthFormProps = PaperProps & CustomProps;

function AuthForm(props: AuthFormProps) {
  const { css, cssimg } = props;

  const navigate = useNavigate();

  return (
    <Paper className={css} radius="md" p="xl" withBorder {...props}>
      <img className={cssimg} src={authImg} alt='auth'></img>
      <Divider labelPosition="center" my="lg" />

      <Button variant="filled" onClick={() => navigate('/lk')}>Вход</Button>
    </Paper>
  );
}

export default AuthForm;