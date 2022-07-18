// in src/rooms.js
import React, { FC } from 'react';
import {
  List,
  Datagrid,
  TextField,
  EditButton,
  TextInput,
  FunctionField,
  SelectInput
} from 'react-admin';
const postFilters = [
  <TextInput source="name" label="Tìm kiếm" alwaysOn />,
  <SelectInput source="type_room" label="Loại phòng" choices={[
    { id: 0, name: 'Cơ sở' },
    { id: 1, name: 'Tòa nhà' },
    { id: 2, name: 'Khu vực' },
    { id: 3, name: 'Tầng' },
    { id: 4, name: 'Phòng' },
  ]} />
];

export const RoomList = () => (
  <List filters={postFilters}>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="name" label="Tên phòng" />
      <TextField source="parent_name" label="Nhóm cha"/>
      <FunctionField source="type_room"
        label="Loại phòng"
        render={(record?: any) => record ?
          `${record.type_room === 0 ? "Cơ sở" :
            record.type_room === 1 ? "Tòa nhà" :
              record.type_room === 2 ? "Khu vực" :
                record.type_room === 3 ? "Tầng" :
                  record.type_room === 4 ? "Phòng" :
                    record.type_room + " chưa rõ"}` : null}
      />
      <EditButton label="Sửa" />
    </Datagrid>
  </List>
);
