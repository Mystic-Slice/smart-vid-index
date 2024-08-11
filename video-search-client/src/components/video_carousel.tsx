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

export function CarouselDemo({ links }: { links: string[] }) {
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
      const vid_iframe = document.getElementById(`video-iframe-${api.previousScrollSnap()}`) as HTMLIFrameElement;
      vid_iframe.contentWindow?.postMessage('{"event":"command","func":"pauseVideo","args":""}', '*');      
    });

  }, [api]);

  return (
    <Carousel className="w-full max-w-sm h-full bg-blue-300" setApi={setApi}>
      <CarouselContent className="bg-yellow-400 h-full">
        {links.map((link, index) => (
          <CarouselItem key={index}>
              <Card>
                <CardContent className="flex bg-red-200 items-center justify-center p-0">
                  <iframe
                    id={`video-iframe-${index}`}
                    src={link + "?version=3&enablejsapi=1"}
                    title={`video-${index}`}
                    className="w-full h-full"
                  />
                </CardContent>
              </Card>
          </CarouselItem>
        ))}
      </CarouselContent>
      <CarouselPrevious />
      <CarouselNext />
      <div className="flex justify-center mt-4">
        {Array.from({ length: count }).map((_, index) => (
          <span
            key={index}
            className={`inline-block w-3 h-3 rounded-full bg-gray-400 mx-2 ${
            index + 1 === current ? "bg-[#291bf0]" : ""
            }`}
            onClick={() => api && api.scrollTo(index)}
          />
        ))}
      </div>
    </Carousel>
  )
}