import React, { useState } from 'react';

const Sidebar = ({ isOpen, menuItems }: { isOpen: boolean, menuItems: any[] }) => {
    // const menuItems = [
    //     "Home",
    //     "Profile",
    //     "Settings",
    //     "Messages"
    //   ];
    
      return (
        <div 
          className={`fixed top-0 left-0 h-screen bg-gray-800 text-white transition-all duration-300 
            ${isOpen ? 'w-[20%]' : 'w-16'}`}
        >
          <div className="p-4">
            <ul className="space-y-2">
              {menuItems.map((item, index) => (
                <li key={index} className={`
                  ${isOpen 
                    ? 'hover:bg-gray-700 p-2 rounded transition-colors duration-200' 
                    : 'text-center font-bold text-xl py-2'}
                `}>
                  {isOpen ? item : item[0]}
                </li>
              ))}
            </ul>
          </div>
        </div>
      );
}

export default Sidebar;