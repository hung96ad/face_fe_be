import React from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
  SelectInput,
  ReferenceInput,
  AutocompleteInput,
  List,
  Datagrid,
  TextField,
  FunctionField,
  EditButton,
  useRecordContext,
  Labeled,
} from 'react-admin';
import { Rooms } from '../types';

const RoomListItem = (props: any) => {
  const record = useRecordContext(props);
  return (
    <Labeled label="Nhóm phòng con" fullWidth>
      <List filter={{ parent_id: record.id }} title={' '}>
        <Datagrid rowClick="edit">
          <TextField source="id" />
          <TextField source="name" label="Tên phòng" />
          <TextField source="parent_name" label="Nhóm cha" />
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
    </Labeled>)
};

export const RoomEdit = () => (
  <Edit>
    <SimpleForm>
      <TextInput disabled source="id" />
      <TextInput source="name" />
      <ReferenceInput source="parent_id" label="Nhóm cha" reference="rooms">
        <AutocompleteInput
          optionText={(choice?: Rooms) =>
            choice?.id
              ? `${choice.name}`
              : ''
          }
        />
      </ReferenceInput>
      <SelectInput source="type_room" disabled choices={[
        { id: 0, name: 'Cơ sở' },
        { id: 1, name: 'Tòa nhà' },
        { id: 2, name: 'Khu vực' },
        { id: 3, name: 'Tầng' },
        { id: 4, name: 'Phòng' },
      ]} />
      <RoomListItem />
    </SimpleForm>
  </Edit>
);