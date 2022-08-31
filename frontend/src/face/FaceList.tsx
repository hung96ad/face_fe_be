// in src/Faces.js
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
import Aside from './RoomAside';
import TagList from './tag';
const postFilters = [
  <TextInput source="q" label="Tìm kiếm" alwaysOn />
];

export const FaceList: FC = (props: any) => {
  return (
    <List {...props} filters={postFilters} aside={<TagList />}>
      <Datagrid optimized rowClick="edit" sx={{
        '& .column-groups': {
          md: { display: 'none' },
          lg: { display: 'table-cell' },
        },
      }}>
        <TextField source="id" />
        <TextField source="name" label="Tên" />
        <ReferenceField source="id_room" label="Tên phòng" reference="rooms">
          <TextField source="name" />
        </ReferenceField>
        <BooleanField source="status" />
        <EditButton label="Sửa" />
      </Datagrid>
    </List>
  )
};
