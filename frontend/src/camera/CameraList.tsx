// in src/Cameras.js
import React, { FC } from 'react';
import {
  List,
  Datagrid,
  TextField,
  EditButton,
  TextInput,
  BooleanField,
  ReferenceField
} from 'react-admin';
const postFilters = [
  <TextInput source="q" label="Tìm kiếm" alwaysOn />
];

export const CameraList: FC = (props: any) => (
  <List {...props} filters={postFilters}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="name" label="Tên camera" />
      <ReferenceField source="id_room" label="Tên phòng" reference="rooms">
        <TextField source="name" />
      </ReferenceField>
      <BooleanField source="status" />
      <EditButton label="Sửa" />
    </Datagrid>
  </List>
);
