'use client'

import {Button, Form, Input, Modal, Select, Space, Table} from "antd";
import {useEffect, useState} from "react";
import axios from "axios";
import { get } from "@/utils/requests";

export default function ReplayTask() {
    const [option, setOption] = useState([]);
    const [selectValue, setSelectValue] = useState("");
    const [groupOption, setGroupOption] = useState([]);
    const [taskList, setTaskList] = useState([]);
    const [defaultSelectValue, setDefaultSelectValue] = useState({});//默认选中的值
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [form] = Form.useForm();
    const handleOk = async () => {
    //     create-task
    //     获取当前下拉框里面的数据值
    //     获取form表单里面的数据
        form.validateFields().then(async (values) => {
            console.log(values);
            const res = await get('http://127.0.0.1:8000/account/create-task?phoneNumber=+'+selectValue+'&chatId='+values.chat_id+'&targetId='+values.target_id)
            // 关闭窗口
            setIsModalVisible(false);
            form.resetFields();
            getTaskList()
            // const res = await axios.post('http://
        })

    }
    const handleCancel = () => {
        setIsModalVisible(false);
        form.resetFields();
    }
    const request = async()=>{
        const accountsRes = await get('http://127.0.0.1:8000/account/get-account-pool')
        console.log(accountsRes.data);

        const options = await accountsRes.data.account_pool.map((item) => ({
            value: item.phone_number.toString(),
            title: item.phone_number.toString(),
            label: item.phone_number.toString(),
        }));
        setOption(options);
        setSelectValue(options[0].value);

    }
   const addTask = ()=>{
        setIsModalVisible(true);
       getGroupList()

   }
    const getGroupList = async()=>{
        console.log(option)
        const res = await get('http://127.0.0.1:8000/account/get-group-phone?phone_number=+'+selectValue)
        console.log(res.data);
        // const groupsWithKey = res.data.groups.map(group => ({
        //     ...group,
        //     key: group.id // 确保每个 group 有唯一的 key
        // }));
        // {
        //     "id": 400,
        //     "group_type": "ChatType.CHANNEL",
        //     "account_id": 1,
        //     "group_name": "全网vip总动员",
        //     "group_id": -1001987173128
        // },
        const groupsWithKey = res.data.groups.map(group => ({
            ...group,
            key: group.id, // 确保每个 group 有唯一的 key
            value: group.group_id,
            title: group.group_name,
            label: group.group_name,
        }));
        setGroupOption(groupsWithKey);


    }
    const getTaskList = async()=>{
        console.log(option)
        const res = await get('http://127.0.0.1:8000/account/get-task-by-id?phoneNumber=+'+selectValue)
        console.log(res.data);
        if (res.data.tasks.length === 0) {
            setTaskList([]);
            return;
        }
        const groupsWithKey = res.data.tasks.map(group => ({
            ...group,
            key: group.id // 确保每个 group 有唯一的 key
        }));
        setTaskList(groupsWithKey);


    }

    useEffect(() => {
        console.log("Options updated:", option);
    }, [option]);
    useEffect(() => {
        console.log("selectValue updated:", selectValue);
        if (selectValue) {
            getTaskList()
        }

    }, [selectValue]);
    useEffect(() => {
        document.title = '群组管理';
        request().then(r => {})

    }, []);

    const syncMessage=(record) =>{
        const id = record.id;
        const res = get('http://127.0.0.1:8000/group/syncMessage?task_id='+id)
    }

    const columns = [
        {
            title: "id",
            dataIndex: "id",
            key: "id"

        },
        {
            title: "账号id",
            dataIndex: "account_id",
            key: "account_id"
        },
        {
            title: "来源群组id",
            dataIndex: "chat_id",
            key: "chat_id"
        },
        {
            title: "目标群组id",
            dataIndex: "target_id",
            key: "target_id",
        },
        {
            title: "操作",
            key: "action",
            render: (text, record) => (
                <Space size="middle">
                    <a onClick={() => syncMessage(record)}>同步消息</a>
                    <a>删除</a>
                </Space>
            )
        }
    ]
    const handleChange = (value)=>{
        console.log("selectValue:",value);
        setSelectValue(value);
    }
    return (
        <div >
            <Select
            onChange={handleChange}
            options={option}
            defaultValue={defaultSelectValue}
            placeholder="请选择"
            value={selectValue}
            className={"w-52 m-2"}
            />

            <Button
                onClick={addTask}
                className={"m-2"}
                >添加任务</Button>

            <Table
                className={"m-2"}
                columns={columns}
                dataSource={taskList}
            >

            </Table>


            <Modal title="添加任务" open={isModalVisible} onOk={handleOk} onCancel={handleCancel}>
                <Form form={form} layout="vertical">
                    <Form.Item
                        name="chat_id"
                        label="来源群组"
                    >
                        <Select 
                            options={groupOption} 
                            showSearch
                            filterOption={(input, option) =>
                                (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
                            }
                        />
                    </Form.Item>
                    <Form.Item
                        name="target_id"
                        label="目标群组"
                    >
                        <Select 
                            options={groupOption} 
                            showSearch
                            filterOption={(input, option) =>
                                (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
                            }
                        />
                    </Form.Item>

                </Form>
            </Modal>
        </div>
    );
}
