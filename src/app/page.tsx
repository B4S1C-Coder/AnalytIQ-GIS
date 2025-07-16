import { ModeToggle } from "@/components/theme-toggle";
import { Button } from "@/components/ui/button";
import { Card, CardAction, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  NavigationMenuViewport,
} from "@/components/ui/navigation-menu"

export default function Landing() {

  return (
  <NavigationMenu className="w-full">
    <NavigationMenuList>
      <NavigationMenuItem>
        <Button variant="ghost">Home</Button>
      </NavigationMenuItem>

      <NavigationMenuItem>
        <NavigationMenuTrigger>About Us</NavigationMenuTrigger>
        <NavigationMenuContent>
          <Card className="w-full max-w-sm">
            <CardHeader>
              <CardTitle>About Us</CardTitle>
              <CardDescription>Something about this project</CardDescription>
              <CardAction>Action</CardAction>
            </CardHeader>
            <CardContent>
              <p>Some Content here that explains what this project is actually doing.</p>
            </CardContent>
            <CardFooter>
              <p>Footer content goes here</p>
            </CardFooter>
          </Card>
        </NavigationMenuContent>
      </NavigationMenuItem>

      <NavigationMenuItem>
        <NavigationMenuTrigger>Item One</NavigationMenuTrigger>
        <NavigationMenuContent>
          <NavigationMenuLink>Link</NavigationMenuLink>
        </NavigationMenuContent>
      </NavigationMenuItem>
      <NavigationMenuItem>
        <ModeToggle />
      </NavigationMenuItem>
    </NavigationMenuList>
  </NavigationMenu>
  );
}