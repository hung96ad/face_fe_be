import React, { FC } from 'react';
import {
  Edit,
  SimpleForm,
  TextInput,
  SelectInput,
  ReferenceInput,
  BooleanInput,
  useRecordContext,
  Labeled,
  List,
  Datagrid,
  TextField,
  BooleanField,
  ImageField,
  FunctionField,
  ImageInput
} from 'react-admin';
import { BASE_URL } from '../configuration/config';

const FaceImages = (props: any) => {
  const record = useRecordContext(props);
  return (
    <Labeled label="Danh sách ảnh" fullWidth>
      <List filter={{ id_face: record.id }} title={' '} resource='face_images'>
        <Datagrid>
          <TextField source="id" />
          <BooleanField source="status" />
          <FunctionField
            label="Image"
            render={(record: any) => {
              return (
                <img style={{ "width": "400px" }} src={`${BASE_URL}${record.path}`}
                />
              );
            }}
          />;
        </Datagrid>
      </List>
    </Labeled>)
};

export const FaceEdit: FC = (props: any) => (
  <Edit {...props}>
    <SimpleForm>
      <TextInput source="name" required />
      <ReferenceInput source="id_room" label="Phòng" reference="rooms">
        <SelectInput optionText="name" required />
      </ReferenceInput>
      <BooleanInput source="status" />
      <ImageInput source="file" label="Related pictures" accept="image/*">
        <ImageField source="src" title="title" />
      </ImageInput>
      <FaceImages />
    </SimpleForm>
  </Edit>
);