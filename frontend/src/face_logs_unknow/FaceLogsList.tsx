import React, { FC } from 'react';
import {
  List,
  TextField,
  ImageField,
  Datagrid,
  ReferenceField
} from 'react-admin';

export const FaceLogsList: FC = (props: any) => {
  return (
    <List {...props}>
      <Datagrid>
        <TextField source="time_created" label="Time" />
        <ReferenceField source="camera_id" label="Camera" reference="cameras">
          <TextField source="name" />-
          <ReferenceField source="id_room" label="Room" reference="rooms">
            <TextField source="full_path" />
          </ReferenceField>
        </ReferenceField>
        <ReferenceField source="face_id" label="Name" reference="faces">
          <TextField source="name" />
        </ReferenceField>
        <TextField source="face_id" label="Face ID" />
        <ImageField source="face_url" title="title" />
      </Datagrid>
    </List>
  )
};
