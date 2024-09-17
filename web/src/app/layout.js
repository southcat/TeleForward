'use client'
import React from 'react';
import { Layout } from 'antd';
import Sidebar from '../components/Sidebar';
import 'antd/dist/reset.css'; // or 'antd/dist/antd.less'
const { Header, Content, Footer, Sider } = Layout;
import '@/style/globals.css'
import { AntdRegistry } from '@ant-design/nextjs-registry';
// import 'antd/dist/antd.css';

const RootLayout = ({ children }) => {
    return (
        <html>
            <body>

                <AntdRegistry>
                    <Layout style={{ minHeight: '100vh',backgroundColor: 'white' }}>
                    <Sider>
                        <Sidebar />
                    </Sider>
                    <Layout>
                        <Header style={{ background: '#fff', padding: 0 }}>
                            <h1>My Application</h1>
                        </Header>
                        <Content style={{ margin: '16px' }}>
                            {children}
                        </Content>
                        <Footer style={{ textAlign: 'center' }}>
                            &copy; 2024 My Application
                        </Footer>
                    </Layout>
                </Layout></AntdRegistry>
            </body>
        </html>
    );
};

export default RootLayout;