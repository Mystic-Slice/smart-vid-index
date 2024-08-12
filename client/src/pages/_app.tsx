import { GeistSans } from "geist/font/sans";
import { type AppType } from "next/app";
import { ToastContainer } from "react-toastify";

import "~/styles/globals.css";
import 'react-toastify/dist/ReactToastify.css';

const MyApp: AppType = ({ Component, pageProps }) => {
  return (
    <div className={GeistSans.className}>
      <Component {...pageProps} />
      <ToastContainer />
    </div>
  );
};

export default MyApp;
