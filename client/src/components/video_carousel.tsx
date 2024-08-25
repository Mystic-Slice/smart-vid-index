import * as React from "react"

import { Card, CardContent } from "~/components/ui/card"
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
  type CarouselApi,
} from "~/components/ui/carousel"

export function YTVideoCarousel({ links, carousel_index }: { links: string[], carousel_index: number }) {
  const [api, setApi] = React.useState<CarouselApi>();
  const [current, setCurrent] = React.useState(0);
  const [count, setCount] = React.useState(0);

  React.useEffect(() => {
    if (!api) {
      return;
    }
  
    setCount(api.scrollSnapList().length);
    setCurrent(api.selectedScrollSnap() + 1);
  
    api.on("select", () => {
      setCurrent(api.selectedScrollSnap() + 1);
    });

    // stop the yt video when the carousel is scrolled
    api.on("scroll", () => {
      const vid_iframe = document.getElementById(`video-iframe-${carousel_index}-${api.previousScrollSnap()}`) as HTMLIFrameElement;
      vid_iframe.contentWindow?.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');      
    });

  }, [api]);

  return (
    <div className="flex flex-col">
      <Carousel className="w-[500px] h-[300px]" setApi={setApi}>
        <CarouselContent>
          {links.map((link, index) => (
            <CarouselItem key={index} className="flex justify-center">
              <iframe
                id={`video-iframe-${carousel_index}-${index}`}
                src={link + "?version=3&enablejsapi=1"}
                title={`video-${index}`}
                className="w-[500px] h-[300px]"
                allowFullScreen
              />
            </CarouselItem>
          ))}
        </CarouselContent>
        <CarouselPrevious />
        <CarouselNext />
      </Carousel>
            
      <div className="flex justify-center mt-4">
        {Array.from({ length: count }).map((_, index) => (
          <span
            key={index}
            className={`inline-block w-3 h-3 rounded-full mx-2 ${
            index + 1 === current ? "bg-[#291bf0]" : "bg-gray-400"
            }`}
            onClick={() => api && api.scrollTo(index)}
          />
        ))}
      </div>
    </div>
  )
}
