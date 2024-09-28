# Задание

**FHIR** - стандарт, описывающий объекты в области медицины в виде ресурсов. В задаче будут использованы 2 типа:

**Patient** - содержит информацию о пациенте (http://hl7.org/fhir/R4/patient.html);
**Appointment** - определяет запись пациента на прием к врачу (http://hl7.org/fhir/R4/appointment.html);

Необходимо вывести список из пациентов в виде карточек, в которых должна содержаться следующая информация:

* имя пациента - `Patient.name[0].text`. Если поле текст отсутствует, то собрать имя конкатенацией `Patient.name[0].family` и `Patient.name[0].given`;
* пол - `Patient.gender`;
* дата рождения - `Patient.birthDate`;
* количество записей на прием - количество ресурсов `Appointment`, которые имеют ссылку на конкретного пациента;
* дата и время приема - `Appointment.start` и `Appointment.description` для каждого `Appointment`;

# API

Для получения записей на прием - https://hapi.fhir.org/baseR4/Appointment?_count=10
Для полученя пациентов - http://hapi.fhir.org/baseR4/Patient/{PatientID}. `PatientID` взять из `Appointment.participant[].actor.reference` и сделать подзапрос.

Обратите внимание, для одного пациента может быть несколько записей.

# Примечание

В случае недоступности тестового сервера необходимо использовать приложенные тестовые ресурсы Appointment и Patient (в файлах *.json). Получение ресурсов можно эмулировать любым удобным способом при условии, что сохраняется асинхронный режим получения их, как если работа велась бы с реальным HTTP сервером.


## Прочее

- предполагается, что актуальные данные о пациентах, после их добавления в БД из запроса. Т.е. не над каждый раз запрашивать данные о пациентах

uvicorn main:app --reload
alembic revision --autogenerate -m "Create initial tables"
alembic upgrade head   