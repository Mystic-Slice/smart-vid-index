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

  // sort items by title
  items.sort((a, b) => a.title.localeCompare(b.title));

return (
    <div 
      className={`fixed top-0 left-0 h-screen transition-all duration-300 text-my-black border-r-4 border-my-grey
        ${isOpen ? 'w-[25%]' : 'w-[10%]'}`}
    >
      <div className="justify-between items-center p-2 mt-3">
        <div className="text-xl">{title}</div>
        {
          isOpen && (
            <div className='flex text-black space-x-2 mt-3'>
            <Input value={inputUrl} onChange={(e) => setInputUrl(e.target.value)} placeholder='Enter URL of a video or playlist' />
            <button 
              onClick={() => {
                addItem(inputUrl)
                setInputUrl('')
              }}
              className='w-[45px] border-2 border-my-accent text-my-accent hover:bg-my-accent hover:text-my-white rounded-full flex items-center justify-center'
            >
              {
                isAdding ? (
                  <ClipLoader size={20} color='var(--my-accent)' className='items-center' />
                ) : (
                  <Plus size={20} />
                )
              }
            </button>
          </div>
          )
        }        
      </div>
      <div className="border-t-2 border-my-grey p-0"></div>
      {
        isProcessing ? (
          <div className="flex justify-center items-center h-full">
            <ClipLoader color="var(--my-accent)" size={50} />
          </div>
        ) : (
          <div className='overflow-hidden p-2 p-t-0'>
            <ScrollArea className="h-[calc(100vh-6rem)]">
              {items.map((item, index) => (
                <div key={index} className={`
                  ${isOpen 
                    ? 'p-2 rounded transition-colors duration-200' 
                    : 'text-center text-xl py-2'}
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
            <div className="flex items-center w-[340px] h-[50px]">
                <div className="w-[100%] overflow-ellipsis overflow-hidden whitespace-nowrap" title={item.title}>
                    {item.title}
                </div>
                <div className="flex">
                    {itemActions.map((action: any, index: number) => (
                        <button key={index} title={action.tooltip} onClick={() => action.handler(item)} className='h-[50px] border-2 border-my-white hover:border-my-accent rounded-full p-3'>
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
        <div className="p-0 text-left text-ellipsis text-nowrap text-base"  title={item.title}>
            {item.title}
        </div>
    )
}


export default Sidebar;