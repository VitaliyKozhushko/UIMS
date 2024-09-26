import os

# Пути к файлам .env
common_env_file = './.env' # итоговый .env
backend_env_file = './backend/.env.backend.docker' # .env для бэка
frontend_env_file = './frontend/.env' # .env для фронта

def merge_env_files(source_file, target_file):
    """
    Добавляет переменные из source_file в target_file, избегая дублирования.
    """

    if not os.path.exists(source_file):
        print(f'Файл {source_file} не найден, переход к следующему файлу .env в списке.')
        return

    existing_vars = []

    with open(source_file, 'r') as source:
        for line in source:
            if not line.strip() or line.startswith('#'):
                continue

            var = line.strip()
            existing_vars.append(var)

    with open(target_file, 'a') as target:
        for var in existing_vars:
            target.write(f'{var}\n')


def main():
    # Очищаем файл перед первым открытием
    with open(common_env_file, 'w') as f:
        pass

    # Объединяем файлы
    merge_env_files(backend_env_file, common_env_file)
    merge_env_files(frontend_env_file, common_env_file)

if __name__ == '__main__':
    main()
