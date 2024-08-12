import React, { useState } from 'react';
import { ClipLoader } from 'react-spinners';
import { ScrollArea } from './ui/scroll-area';
import { Input } from './ui/input';
import { Plus } from 'lucide-react';

const Sidebar = ({ 
    isOpen, 
    items, 
    isProcessing, 
    title, 
    itemActions,  
    addItem,
    isAdding,
}: { 
  isOpen: boolean, 
  items: any[], 
  isProcessing: boolean, 
  title: string, 
  itemActions: any,
  addItem: any,
  isAdding: boolean,
}) => {

  const [inputUrl, setInputUrl] = useState('');

return (
    <div 
      className={`fixed top-0 left-0 h-screen bg-gray-800 text-white transition-all duration-300 
        ${isOpen ? 'w-[30%]' : 'w-32'}`}
    >
      <div className="justify-between items-center p-4">
        <div className="font-bold text-xl">{title}</div>
        {
          isOpen && (
            <div className='flex text-black'>
            <Input value={inputUrl} onChange={(e) => setInputUrl(e.target.value)} />
            <button 
              onClick={() => {
                addItem(inputUrl)
                setInputUrl('')
              }}
            >
              {
                isAdding ? (
                  <ClipLoader color="#999" size={20} />
                ) : (
                  <Plus size={20} />
                )
              }            
            </button>
          </div>
          )
        }        
      </div>
      {
        isProcessing ? (
          <div className="flex justify-center items-center h-full">
            <ClipLoader color="#999" size={50} />
          </div>
        ) : (
          <div className='flex-1 overflow-hidden'>
            <ScrollArea className="h-[calc(100vh-4rem)] rounded-md border p-4 overflow-y-auto">
              {items.map((item, index) => (
                <div key={index} className={`
                  ${isOpen 
                    ? 'hover:bg-gray-700 p-2 rounded transition-colors duration-200' 
                    : 'text-center font-bold text-xl py-2'}
                `}>
                  {isOpen ? itemOpenView(item, itemActions) : itemClosedView(item, itemActions)}
                </div>
              ))}
            </ScrollArea>
          </div>
        )
      }
    </div>
  );
}

const itemOpenView = (item: any, itemActions: any) => {
    return (
        <>
            <div className="flex items-center">
                <div className="flex-1">
                    {item.title}
                </div>
                <div className="flex">
                    {itemActions.map((action: any, index: number) => (
                        <button key={index} onClick={() => action.handler(item)}>
                            {action.icon}
                        </button>
                    ))}
                </div>
            </div>
        </>
    )
}

const itemClosedView = (item: any, itemActions: any) => {
    return (
        <div className="w-20 h-10 p-0 text-ellipsis text-nowrap text-sm">
            {item.title}
        </div>
    )
}


export default Sidebar;