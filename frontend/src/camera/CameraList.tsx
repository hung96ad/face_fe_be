// in src/Cameras.js
import React, { FC } from 'react';
import {
  List,
  Datagrid,
  TextField,
  EditButton,
  TextInput,
  BooleanField,
  ReferenceField,
  SelectInput
} from 'react-admin';
const postFilters = [
  <TextInput source="q" label="Tìm kiếm" alwaysOn />,
  <SelectInput source="id_room" label="Loại phòng" choices={[
    { id: 0, name: 'Cơ sở' },
    { id: 1, name: 'Tòa nhà' },
    { id: 2, name: 'Khu vực' },
    { id: 3, name: 'Tầng' },
    { id: 4, name: 'Phòng' },
  ]} />
];

export const CameraList: FC = (props: any) => (
  <List {...props} filters={postFilters}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="name" label="Tên camera" />
      <ReferenceField source="id_room" label="Tên phòng" reference="rooms">
        <TextField source="name" />
      </ReferenceField>
      <TextField source="service_type" label="Loại camera" />
      <BooleanField source="status" />
      <EditButton label="Sửa" />
    </Datagrid>
  </List>
);
