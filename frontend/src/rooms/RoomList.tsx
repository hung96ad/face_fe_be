import * as React from 'react';
import { Fragment, useState } from 'react';
import {
    ListBase,
    ListActions,
    useListContext,
    EditButton,
    Title,
} from 'react-admin';
import {
    Box,
    List,
    ListItem,
    ListItemText,
    ListItemSecondaryAction,
    Collapse,
    Card,
} from '@mui/material';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import CreateRoomButton from './CreateRoomButton';

const RoomList = () => (
    <ListBase perPage={10000}>
        <ListActions />
        <Box marginTop="1em">
            <Card>
                <Tree />
            </Card>
        </Box>
    </ListBase>
);

const Tree = () => {
    const { data, defaultTitle } = useListContext();
    const [openChildren, setOpenChildren] = useState<any[]>([]);
    const toggleNode = (node: any) =>
        setOpenChildren((state: any[]) => {
            if (state.includes(node.id)) {
                return [
                    ...state.splice(0, state.indexOf(node.id)),
                    ...state.splice(state.indexOf(node.id) + 1, state.length),
                ];
            } else {
                return [...state, node.id];
            }
        });
    const roots = data
        ? data.filter(node => typeof node.parent_id === 'undefined')
        : [];
    const getChildNodes = (root: any) =>
        data.filter(node => node.parent_id === root.id);
    return (
        <List>
            <Title defaultTitle={defaultTitle} />
            {roots.map(root => (
                <SubTree
                    key={root.id}
                    root={root}
                    getChildNodes={getChildNodes}
                    openChildren={openChildren}
                    toggleNode={toggleNode}
                    level={1}
                />
            ))}
        </List>
    );
};
interface SubTreeProps {
    key: any
    level: number
    root: any
    getChildNodes: any
    openChildren: any
    toggleNode: any
}
const SubTree = (props: SubTreeProps) => {
    const childNodes = props.getChildNodes(props.root);
    const hasChildren = childNodes.length > 0;
    const open = props.openChildren.includes(props.root.id);
    return (
        <Fragment>
            <ListItem
                onClick={() => hasChildren && props.toggleNode(props.root)}
                style={{ paddingLeft: props.level * 16 }}
            >
                {hasChildren && open && <ExpandLess />}
                {hasChildren && !open && <ExpandMore />}
                {!hasChildren && <div style={{ width: 24 }}>&nbsp;</div>}
                <ListItemText primary={props.root.name} />

                <ListItemSecondaryAction>
                    <EditButton record={props.root} />
                    <CreateRoomButton record={props.root} />
                </ListItemSecondaryAction>
            </ListItem>
            <Collapse in={open} timeout="auto" unmountOnExit>
                <List component="div" disablePadding>
                    {childNodes.map((node: any) => (
                        <SubTree
                            key={node.id}
                            root={node}
                            getChildNodes={props.getChildNodes}
                            openChildren={props.openChildren}
                            toggleNode={props.toggleNode}
                            level={props.level + 1}
                        />
                    ))}
                </List>
            </Collapse>
        </Fragment>
    );
};

export default RoomList;